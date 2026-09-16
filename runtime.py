from __future__ import annotations

from dataclasses import dataclass, fields, is_dataclass
from enum import Enum
from typing import Any, ClassVar, Iterable

MAX_SOLVER_DEPTH = 48
MAX_CANDIDATES = 128


# ---------------------------------------------------------------------------
# Semantic products
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Product:
    terms: frozenset[str]

    def __mul__(self, other: Any) -> "Product":
        return self | sem(other)

    def __or__(self, other: "Product") -> "Product":
        return Product(self.terms | other.terms)

    def __contains__(self, term: Any) -> bool:
        return semantic_name(term) in self.terms

    def __iter__(self):
        return iter(sorted(self.terms))

    def __str__(self) -> str:
        return " × ".join(sorted(self.terms)) if self.terms else "∅"


EMPTY = Product(frozenset())


def product_names(names: Iterable[str]) -> Product:
    return Product(frozenset(names))


def semantic_name(term: Any) -> str:
    if isinstance(term, AxisValue):
        return term.name
    if isinstance(term, str):
        return term
    if isinstance(term, SemanticEnum):
        raise TypeError("surface enum values expand to products; use sem(value)")
    if isinstance(term, SemanticModelMeta):
        return term.__name__
    if hasattr(term, "_semantic_name"):
        return str(term._semantic_name)
    raise TypeError(f"not a semantic term: {term!r}")


def sem(*terms: Any) -> Product:
    out = EMPTY
    for term in terms:
        if term is None:
            continue
        if isinstance(term, Product):
            out = out | term
        elif isinstance(term, SemanticEnum):
            out = out | term._semantics
        elif isinstance(term, SemanticModelMeta):
            # In queries, a model class means the semantic region represented by
            # that class, not merely its spelling.
            out = out | term._semantics
        else:
            out = out | Product(frozenset({semantic_name(term)}))
    return out


class SemanticModelMeta(type):
    def __mul__(cls, other: Any) -> Product:
        return sem(cls) * other

    def __rmul__(cls, other: Any) -> Product:
        return sem(other) * cls


class SemanticModel(metaclass=SemanticModelMeta):
    _semantics: ClassVar[Product] = EMPTY


@dataclass(frozen=True, slots=True)
class AxisValue:
    axis: str
    value: str

    @property
    def name(self) -> str:
        return f"{self.axis}.{self.value}"

    def __mul__(self, other: Any) -> Product:
        return sem(self) * other

    def __rmul__(self, other: Any) -> Product:
        return sem(other) * self

    def __str__(self) -> str:
        return self.name


class SemanticAxis:
    _axis_name: ClassVar[str]
    _cardinality: ClassVar[str]
    _applies: ClassVar[Any] = None


class SemanticEnum(Enum):
    _semantic_map: ClassVar[dict[str, Product]]

    @property
    def _semantics(self) -> Product:
        return getattr(self.__class__, "_semantic_map", {}).get(self.name, EMPTY)


# ---------------------------------------------------------------------------
# Rule expressions
#
# A rule expression is a small boolean formula over the presence of semantic
# factors in a product. It is declarative data, not class inheritance logic.
# ---------------------------------------------------------------------------


class Expr:
    def evaluate(self, terms: frozenset[str]) -> bool:
        raise NotImplementedError

    def forced_terms(self) -> set[str]:
        return set()


@dataclass(frozen=True, slots=True)
class Term(Expr):
    name: str

    def evaluate(self, terms: frozenset[str]) -> bool:
        return self.name in terms

    def forced_terms(self) -> set[str]:
        return {self.name}

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True, slots=True)
class All(Expr):
    items: tuple[Expr, ...]

    def evaluate(self, terms: frozenset[str]) -> bool:
        return all(item.evaluate(terms) for item in self.items)

    def forced_terms(self) -> set[str]:
        out: set[str] = set()
        for item in self.items:
            out |= item.forced_terms()
        return out

    def __str__(self) -> str:
        return f"ALL({', '.join(str(x) for x in self.items)})"


@dataclass(frozen=True, slots=True)
class Any(Expr):
    items: tuple[Expr, ...]

    def evaluate(self, terms: frozenset[str]) -> bool:
        return any(item.evaluate(terms) for item in self.items)

    def __str__(self) -> str:
        return f"ANY({', '.join(str(x) for x in self.items)})"


@dataclass(frozen=True, slots=True)
class Not(Expr):
    item: Expr

    def evaluate(self, terms: frozenset[str]) -> bool:
        return not self.item.evaluate(terms)

    def __str__(self) -> str:
        return f"NOT({self.item})"


TRUE = All(())
FALSE = Any(())


def parse_expr(data: Any, axis_values: dict[str, list[str]] | None = None) -> Expr:
    if data is None:
        return TRUE
    if isinstance(data, Expr):
        return data
    if isinstance(data, bool):
        return TRUE if data else FALSE
    if isinstance(data, str):
        return Term(data)
    if isinstance(data, list):
        return All(tuple(parse_expr(x, axis_values) for x in data))
    if isinstance(data, dict):
        if "term" in data:
            return Term(str(data["term"]))
        if "axis" in data:
            # Compact authoring form: any value of the axis is present.
            values = (axis_values or {}).get(str(data["axis"]), [])
            return Any(tuple(Term(x) for x in values))
        if "all" in data:
            return All(tuple(parse_expr(x, axis_values) for x in data["all"]))
        if "any" in data:
            return Any(tuple(parse_expr(x, axis_values) for x in data["any"]))
        if "not" in data:
            return Not(parse_expr(data["not"], axis_values))
        if "const" in data:
            return TRUE if data["const"] else FALSE
    raise ValueError(f"not a rule expression: {data!r}")


@dataclass(frozen=True, slots=True)
class Rule:
    name: str
    kind: str
    when: Expr = TRUE
    then: Expr = TRUE
    left: Expr = TRUE
    right: Expr = TRUE
    profiles: tuple[str, ...] = ()


# ---------------------------------------------------------------------------
# Relations
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class RelationFact:
    relation: "RelationType"
    operands: tuple["ModelRef", ...]

    def __str__(self) -> str:
        return f"{self.relation.name}({', '.join(x.uid for x in self.operands)})"


@dataclass(frozen=True, slots=True)
class RelationType:
    name: str
    signature: tuple[type[SemanticModel], ...]
    operand_names: tuple[str, ...] = ()
    base: "RelationType | None" = None

    def specializes(self, other: "RelationType") -> bool:
        current: RelationType | None = self
        while current is not None:
            if current is other:
                return True
            current = current.base
        return False

    def __call__(self, *operands: "ModelRef") -> RelationFact:
        if len(operands) != len(self.signature):
            raise TypeError(f"{self.name} expects {len(self.signature)} operands")
        for index, (operand, expected) in enumerate(zip(operands, self.signature)):
            # Operand regions are semantic, not class paths: a representation
            # satisfies the region when it entails the region's product.
            if not expected._semantics.terms <= operand.semantics.terms:
                label = self.operand_names[index] if index < len(self.operand_names) else str(index)
                raise TypeError(
                    f"{self.name} operand {label!r} expects {expected.__name__}, "
                    f"but {operand.model.__name__} does not entail it"
                )
        return RelationFact(self, tuple(operands))


# ---------------------------------------------------------------------------
# Registry and solver
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class StoredDatum:
    subject_uid: str
    representation: type[SemanticModel]
    semantics: Product
    value: SemanticModel


class SemanticRegistry:
    def __init__(self, spec: dict[str, Any], active_profiles: Iterable[str] = ()):
        self.spec = spec
        self.active_profiles = tuple(active_profiles)

        self.axis_of_value: dict[str, str] = {}
        self.axis_cardinality: dict[str, str] = {}
        self.axis_applies: dict[str, Any] = {}
        self.axis_region: dict[str, Expr] = {}
        self.axis_requires: dict[str, Any] = {}
        axis_values: dict[str, list[str]] = {}

        for axis_name, axis in spec.get("axes", {}).items():
            values = [f"{axis_name}.{value}" for value in axis.get("values", [])]
            axis_values[axis_name] = values
            self.axis_cardinality[axis_name] = axis.get("cardinality", "many")
            self.axis_applies[axis_name] = axis.get("applies")
            self.axis_requires[axis_name] = axis.get("requires")
            for value in values:
                self.axis_of_value[value] = axis_name

        self.model_fields: dict[str, list[dict[str, Any]]] = {
            name: list(model.get("fields") or [])
            for name, model in spec.get("models", {}).items()
        }
        self.model_semantics: dict[str, list[str]] = {
            name: list(model.get("semantics") or [])
            for name, model in spec.get("models", {}).items()
        }

        self.codeword_relations: dict[str, str] = dict(spec.get("codeword_relations", {}))
        self.aliases: dict[str, list[str]] = dict(spec.get("aliases", {}))

        # Constraints are implied by declarations. There is no authored rules
        # block: an axis, an axis value, or a concept states applies/requires/
        # disjoint/excludes for itself, and the solver compiles the rule.
        self.rules: list[Rule] = []

        def add_declarations(
            owner: str,
            when: Expr,
            declaration: dict[str, Any],
            axis_scope: str | None = None,
        ) -> None:
            applies = declaration.get("applies")
            if applies:
                region = parse_expr(applies, axis_values)
                if axis_scope is not None:
                    self.axis_region[axis_scope] = region
                self.rules.append(
                    Rule(
                        name=f"{owner}.applies",
                        kind="applicability",
                        when=when,
                        then=region,
                    )
                )
            requires = declaration.get("requires")
            if requires:
                self.rules.append(
                    Rule(
                        name=f"{owner}.requires",
                        kind="requirement",
                        when=when,
                        then=parse_expr(requires, axis_values),
                    )
                )
            for index, right in enumerate(declaration.get("disjoint") or ()):
                self.rules.append(
                    Rule(
                        name=f"{owner}.disjoint.{index}",
                        kind="disjointness",
                        left=when,
                        right=parse_expr(right, axis_values),
                    )
                )
            for index, group in enumerate(declaration.get("excludes") or ()):
                # A group is one co-factor or a list of co-factors.
                items = list(group) if isinstance(group, (list, tuple)) else [group]
                parts = [when] + [parse_expr(item, axis_values) for item in items]
                self.rules.append(
                    Rule(
                        name=f"{owner}.excludes.{index}",
                        kind="exclusion",
                        when=All(tuple(parts)),
                    )
                )

        for axis_name in axis_values:
            axis = spec["axes"][axis_name]
            when_axis = Any(tuple(Term(v) for v in axis_values[axis_name]))
            add_declarations(axis_name, when_axis, axis, axis_scope=axis_name)
            for value_name, declaration in (axis.get("value_meta") or {}).items():
                add_declarations(
                    f"{axis_name}.{value_name}",
                    Term(f"{axis_name}.{value_name}"),
                    declaration,
                )
        for model_name, model in spec.get("models", {}).items():
            add_declarations(model_name, Term(model_name), model)

        self.active_rules = [
            rule
            for rule in self.rules
            if not rule.profiles or set(rule.profiles) & set(self.active_profiles)
        ]
        self.term_applicability: dict[str, list[Expr]] = {}
        for rule in self.active_rules:
            if rule.kind == "applicability" and isinstance(rule.when, Term):
                self.term_applicability.setdefault(rule.when.name, []).append(rule.then)

    # -- property access ----------------------------------------------------

    def fields_of(self, model: type[SemanticModel]) -> list[dict[str, Any]]:
        return self.model_fields.get(model.__name__, [])

    def codeword_relation(self, codeword: Any) -> str | None:
        if isinstance(codeword, SemanticEnum):
            key = f"{type(codeword).__name__}.{codeword.name}"
        else:
            key = str(codeword)
        return self.codeword_relations.get(key)

    # -- closure and legality ----------------------------------------------

    def closure(self, product: Product) -> Product:
        return Product(self._closure(product.terms))

    def _assertion_terms(self, name: str) -> list[str]:
        # A requirement naming a concept asserts that concept's whole semantic
        # ancestry, not merely its spelling.
        return self.model_semantics.get(name) or [name]

    def _closure(self, start: frozenset[str] | set[str]) -> frozenset[str]:
        terms = set(start)
        changed = True
        while changed:
            changed = False
            for rule in self.active_rules:
                if rule.kind not in ("implication", "requirement"):
                    continue
                if not rule.when.evaluate(terms):
                    continue
                for name in rule.then.forced_terms():
                    for term in self._assertion_terms(name):
                        if term not in terms:
                            terms.add(term)
                            changed = True
        return frozenset(terms)

    def consistent(self, terms: frozenset[str], depth: int = 0) -> bool:
        if depth > MAX_SOLVER_DEPTH:
            return False
        by_axis: dict[str, set[str]] = {}
        for term in terms:
            axis = self.axis_of_value.get(term)
            if axis:
                by_axis.setdefault(axis, set()).add(term)
        for axis, values in by_axis.items():
            if self.axis_cardinality.get(axis) == "one" and len(values) > 1:
                return False
        for rule in self.active_rules:
            if rule.kind == "disjointness":
                if rule.left.evaluate(terms) and rule.right.evaluate(terms):
                    return False
            elif rule.kind == "exclusion":
                if rule.when.evaluate(terms):
                    return False
        for rule in self.active_rules:
            if rule.kind not in ("implication", "requirement", "applicability"):
                continue
            if not rule.when.evaluate(terms):
                continue
            if rule.then.evaluate(terms):
                continue
            # A requirement may stay undecided in a partial product. It is
            # illegal only when no completion can satisfy it.
            if not self.satisfiable(rule.then, terms, depth + 1):
                return False
        return True

    def satisfiable(self, expr: Expr, terms: frozenset[str], depth: int = 0) -> bool:
        return bool(self._candidates(expr, terms, depth))

    def _candidates(
        self, expr: Expr, terms: frozenset[str], depth: int
    ) -> list[frozenset[str]]:
        if depth > MAX_SOLVER_DEPTH:
            return []
        if expr.evaluate(terms):
            return [terms]
        if isinstance(expr, Not):
            return [terms] if not expr.item.evaluate(terms) else []
        if isinstance(expr, Any):
            out: list[frozenset[str]] = []
            for item in expr.items:
                out.extend(self._candidates(item, terms, depth + 1))
            return _dedupe(out)
        if isinstance(expr, All):
            frontier: list[frozenset[str]] = [terms]
            for item in expr.items:
                nxt: list[frozenset[str]] = []
                for candidate in frontier:
                    nxt.extend(self._candidates(item, candidate, depth + 1))
                frontier = _dedupe(nxt)[:MAX_CANDIDATES]
                if not frontier:
                    return []
            return frontier
        if isinstance(expr, Term):
            candidate = self._closure(terms | set(self._assertion_terms(expr.name)))
            return [candidate] if self.consistent(candidate, depth + 1) else []
        return []

    def legal(self, product: Product) -> bool:
        return self.consistent(self._closure(product.terms))

    def entails(self, product: Product, wanted: Any) -> bool:
        return self._closure(sem(wanted).terms) <= self._closure(product.terms)

    def equivalent(self, left: Product, right: Product) -> bool:
        return self._closure(left.terms) == self._closure(right.terms)

    def applicable(self, product: Product, term: Any) -> bool:
        # Meaningfulness is emergent: a product gains a dimension when the
        # dimension's region can hold in it, even though the product does not
        # assert that dimension.
        axis_name = _axis_name(term)
        region = self.axis_region.get(axis_name)
        closed = self._closure(product.terms)
        if region is not None and not self.satisfiable(region, closed):
            return False
        for extra in self.term_applicability.get(axis_name, ()):
            if not self.satisfiable(extra, closed):
                return False
        return True


def _axis_name(axis_or_value: Any) -> str:
    if isinstance(axis_or_value, AxisValue):
        return axis_or_value.axis
    if isinstance(axis_or_value, type) and issubclass(axis_or_value, SemanticAxis):
        return axis_or_value._axis_name
    if isinstance(axis_or_value, SemanticModelMeta):
        return axis_or_value.__name__
    return str(axis_or_value)


def _dedupe(items: list[frozenset[str]]) -> list[frozenset[str]]:
    return list(dict.fromkeys(items))


# ---------------------------------------------------------------------------
# Store and references
# ---------------------------------------------------------------------------


class AmbiguousSemanticMatch(LookupError):
    pass


class ModelRef:
    def __init__(self, store: "Store", uid: str, model: type[SemanticModel]):
        self.store = store
        self.uid = uid
        self.model = model

    @property
    def fields(self) -> tuple[str, ...]:
        if not is_dataclass(self.model):
            return ()
        return tuple(f.name for f in fields(self.model))

    @property
    def semantics(self) -> Product:
        return self.model._semantics | self.store._assertions.get(self.uid, EMPTY)

    def assert_(self, *terms: Any) -> "ModelRef":
        extra = sem(*terms)
        candidate = self.semantics | extra
        if not self.store.registry.legal(candidate):
            raise ValueError(f"illegal semantic assertion: {candidate}")
        self.store._assertions[self.uid] = self.store._assertions.get(self.uid, EMPTY) | extra
        return self

    def set(self, value: SemanticModel, *qualifiers: Any) -> SemanticModel:
        return self.store.set(self, value, *qualifiers)

    def get(self, *query: Any) -> SemanticModel:
        return self.store.get(self, *query)

    def find(self, *query: Any) -> list[SemanticModel]:
        return self.store.find(self, *query)

    def __repr__(self) -> str:
        return f"Ref[{self.model.__name__}]({self.uid!r})"


class Store:
    def __init__(self, registry: SemanticRegistry):
        self.registry = registry
        self._data: dict[str, list[StoredDatum]] = {}
        self._assertions: dict[str, Product] = {}
        self._relations: list[RelationFact] = []

    def ref(self, uid: str, model: type[SemanticModel]) -> ModelRef:
        return ModelRef(self, uid, model)

    def set(self, subject: ModelRef, value: SemanticModel, *qualifiers: Any) -> SemanticModel:
        rep = type(value)
        semantics = value_semantics(value) | sem(*qualifiers)
        if not self.registry.legal(semantics):
            raise ValueError(f"illegal datum semantics: {semantics}")
        bucket = self._data.setdefault(subject.uid, [])
        bucket[:] = [d for d in bucket if d.representation is not rep]
        bucket.append(StoredDatum(subject.uid, rep, semantics, value))
        return value

    def find(self, subject: ModelRef, *query: Any) -> list[SemanticModel]:
        wanted = sem(*query)
        out: list[SemanticModel] = []
        for datum in self._data.get(subject.uid, []):
            if self.registry.entails(datum.semantics, wanted):
                out.append(datum.value)
        return sorted(out, key=lambda x: type(x).__name__)

    def get(self, subject: ModelRef, *query: Any) -> SemanticModel:
        if len(query) == 1 and isinstance(query[0], SemanticModelMeta):
            rep = query[0]
            exact = [d.value for d in self._data.get(subject.uid, []) if d.representation is rep]
            if exact:
                return exact[0]
        found = self.find(subject, *query)
        if not found:
            raise KeyError(f"no semantic match for {subject.uid}: {sem(*query)}")
        if len(found) > 1:
            raise AmbiguousSemanticMatch(
                f"{subject.uid}: {sem(*query)} -> {[type(x).__name__ for x in found]}"
            )
        return found[0]

    def get_many(self, subjects: Iterable[ModelRef], *query: Any) -> dict[str, SemanticModel]:
        return {subject.uid: self.get(subject, *query) for subject in subjects}

    def relate(self, relation: RelationType, *operands: ModelRef) -> RelationFact:
        fact = relation(*operands)
        self._relations.append(fact)
        return fact

    def relations(self, relation: RelationType | None = None) -> list[RelationFact]:
        # Querying a base relation returns every fact whose relation
        # specializes it; direction is inherited, so operand order holds.
        if relation is None:
            return list(self._relations)
        return [fact for fact in self._relations if fact.relation.specializes(relation)]


def value_semantics(value: SemanticModel, _seen: frozenset[int] | None = None) -> Product:
    seen = _seen or frozenset()
    if id(value) in seen:
        return EMPTY
    seen = seen | {id(value)}
    out = type(value)._semantics
    if is_dataclass(value):
        for field in fields(value):
            out = out | _nested_semantics(getattr(value, field.name), seen)
    return out


def _nested_semantics(item: Any, seen: frozenset[int]) -> Product:
    if isinstance(item, SemanticEnum):
        return item._semantics
    if isinstance(item, SemanticModel) and is_dataclass(item):
        return value_semantics(item, seen)
    if isinstance(item, (list, tuple)):
        out = EMPTY
        for sub in item:
            out = out | _nested_semantics(sub, seen)
        return out
    return EMPTY
