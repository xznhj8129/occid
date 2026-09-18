from __future__ import annotations

import hashlib
import tempfile
from dataclasses import fields
from pathlib import Path

from compiler import compile_schema
from runtime import Product, sem, value_semantics
import generated.occid2 as occid2
from generated.occid2 import (
    AirTask,
    Airframe,
    Altitude,
    Actor,
    AssignedWork,
    Authority,
    Biological,
    BloodGroup,
    Command,
    CommandOperation,
    Condition,
    ConstrainedBy,
    Directive,
    Drone,
    Geodetic,
    GlobalPosition,
    Holds,
    LocalPosition,
    Machine,
    Mark,
    Mission,
    MOVE,
    Person,
    PhysicalDomain,
    Plan,
    PlainText,
    Position,
    Predicate,
    Realm,
    REGISTRY_SPEC,
    Representation,
    Task,
    TaskIntent,
    TaskTimeWindow,
    TemporalMode,
    Time,
    Timestamp,
    Truth,
    TruthBoolean,
    UAV,
    UID,
    UnmannedVehicle,
    WeatherLimits,
    new_store,
)

ROOT = Path(__file__).parent


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    store = new_store()
    registry = store.registry

    # 1. Parentage provides inherited fields; the word is the only taxonomy.
    task_fields = {field.name for field in fields(Task)}
    check({"uid", "instruction", "intent", "priority", "status"} <= task_fields, "Task field inheritance failed")
    check({"uid", "operation"} <= {field.name for field in fields(Command)}, "Command carries only its word")

    # 2. Aliases are products, not classes. Recursive expansion is canonical.
    check(isinstance(Drone, Product), "Drone must be a product, not a class")
    check(registry.entails(Drone, UnmannedVehicle), "Drone must entail UnmannedVehicle")
    check(registry.entails(Drone, PhysicalDomain.AIR), "Drone must entail PhysicalDomain.AIR")
    check(registry.entails(Drone, Airframe.MULTIROTOR), "Drone must entail its airframe")
    check(Drone == sem(UAV, Airframe.MULTIROTOR), "Drone must equal UAV * Airframe.MULTIROTOR")
    check(Geodetic == sem(Representation.Geodetic), "Geodetic must equal Representation.Geodetic")
    check(registry.equivalent(Drone, sem(UAV, Airframe.MULTIROTOR)), "named and unnamed products must be equivalent")

    # 3. Axis cardinality is automatic; partial products stay legal.
    check(registry.legal(sem(UnmannedVehicle, PhysicalDomain.AIR)), "single-domain partial product is legal")
    check(not registry.legal(sem(UnmannedVehicle, PhysicalDomain.LAND, PhysicalDomain.AIR)), "two domains contradict")

    # 4. The BloodGroup contradiction is derived, not declared.
    check(registry.entails(sem(BloodGroup.A_POS), Biological), "BloodGroup must entail Biological")
    check(not registry.legal(sem(Drone, BloodGroup.A_POS)), "Drone cannot have a blood group")
    check(registry.legal(sem(Person, BloodGroup.A_POS)), "Person accepts a blood group")

    # 5. Substrate cardinality separates living from machine.
    check(not registry.legal(sem(Machine, Actor)), "Machine * Actor clashes on Substrate")

    # 6. Charts produce irreducible variables; units stay metadata.
    check({field.name for field in fields(GlobalPosition)} == {"lat", "lon", "h"}, "geodetic chart fields")
    check(GlobalPosition._units == {"lat": "deg", "lon": "deg", "h": "m"}, "geodetic chart units")
    check({field.name for field in fields(LocalPosition)} == {"x", "y", "z"}, "local cartesian chart fields")
    check({field.name for field in fields(Mark)} == {"uid", "name", "lat", "lon", "h"}, "Mark compiles its chart")

    uav = store.ref("uav-1", UnmannedVehicle)
    uav.set(GlobalPosition(lat=45.30, lon=-74.20, h=125.0))

    # 7. The representation is selected by factors, not by class paths.
    uav.set(LocalPosition(x=120.0, y=-40.0, z=15.0))
    check(len(uav.find(Position)) == 2, "both representations answer the Position question")
    check(uav.get(Position, Representation.Geodetic).lon == -74.20, "geodetic narrowing failed")
    check(uav.get(Position, Representation.LocalCartesian).x == 120.0, "local narrowing failed")

    # 8. Exact class lookup and semantic lookup return the same stored value.
    check(uav.get(GlobalPosition).lat == 45.30, "exact representation lookup failed")

    # 9. A word names an expression; the task realizes it.
    move = store.task(
        "task-move-1", Task, TaskIntent.MOVE, instruction="move to mark alpha"
    )
    check(registry.expression_of(TaskIntent.MOVE) == MOVE, "MOVE word must name MOVE expression")
    check(
        MOVE.factors == sem(Task, Realm.WORLD, TemporalMode.ACHIEVE),
        "MOVE factors must be the declared product",
    )
    check(move.expression.name == "MOVE", "task must realize MOVE")
    check(move.ref.get(Task).intent is TaskIntent.MOVE, "the word stores the vocabulary member")
    check(
        registry.entails(value_semantics(move.ref.get(Task)), MOVE.factors),
        "task value must entail the expression factors",
    )
    check(move.unbound == ["actor", "destination"], "unbound variables")
    move.bind("actor", uav)
    try:
        move.bind("destination", uav)
    except TypeError:
        pass
    else:
        raise AssertionError("a vehicle does not satisfy the Position region")
    mark_ref = store.ref("mark-alpha", Mark)
    mark_ref.set(Mark(uid=UID(uid="mark-alpha"), name=PlainText(value="alpha"), lat=45.28, lon=-74.18, h=110.0))
    move.bind("destination", mark_ref)
    check(move.unbound == [], "all variables bound")

    # 10. An unbound variable is an unknown, not an error.
    target = store.ref("target-42", UnmannedVehicle)
    locate = store.task(
        "task-locate-1", Task, TaskIntent.LOCATE, instruction="locate target-42"
    )
    locate.bind("target", target)
    check(locate.solve() == {}, "an entity without a position has an unknown answer")
    check(target.find(Position) == [], "no datum is unknown, not illegal")
    target.set(GlobalPosition(lat=45.10, lon=-74.40, h=90.0))
    solved = locate.solve()
    check(solved["position"].lat == 45.10, "the answer appears once the fact exists")

    # 11. Relations are directed, roles are named, and operands are validated.
    fact = store.relate(AssignedWork, uav, move.ref)
    check(str(fact) == "AssignedWork(assignee=uav-1, work=task-move-1)", "named roles failed")
    check(fact.operands == (uav, move.ref), "relation operand order lost")
    try:
        AssignedWork(move.ref, uav)
    except TypeError:
        pass
    else:
        raise AssertionError("reversed AssignedWork must fail")
    check(fact in store.relations(AssignedWork), "relation query must see facts")

    # 12. Applicability is emergent and never asserts.
    check(not registry.entails(sem(Altitude), PhysicalDomain.AIR), "applicability must not assert")
    check(registry.legal(sem(Mission, Altitude)), "Mission * Altitude is unknown, not illegal")
    check(registry.legal(sem(Mission, PhysicalDomain.AIR, Altitude)), "Altitude is meaningful in air")
    check(not registry.legal(sem(Mission, PhysicalDomain.SEA, Altitude)), "Altitude is meaningless at sea")
    check(registry.applicable(AirTask, Altitude), "AirTask = Task * AIR gains Altitude")

    # 13. Compiler output is deterministic.
    with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
        compile_schema(ROOT / "occid2.schema.yaml", Path(a))
        compile_schema(ROOT / "occid2.schema.yaml", Path(b))
        for filename in ("occid2.py", "semantic_registry.json"):
            ha = hashlib.sha256((Path(a) / filename).read_bytes()).digest()
            hb = hashlib.sha256((Path(b) / filename).read_bytes()).digest()
            check(ha == hb, f"nondeterministic compiler output: {filename}")

    # 14. Every word resolves to an expression; a command carries only its word.
    for word in REGISTRY_SPEC["word_expressions"]:
        enum_name, member = word.split(".", 1)
        registry.expression_of(getattr(getattr(occid2, enum_name), member))
    cmd = store.task("task-cmd-1", Command, CommandOperation.MOVE)
    check(cmd.expression.name == "DIRECT", "MOVE word must name the DIRECT expression")
    cmd.bind("target", uav)
    cmd.bind("destination", mark_ref)
    check(
        cmd.unbound == ["path", "radius", "speed", "yaw"],
        "unbound motion parameters are unknowns, not columns",
    )

    # 15. Quantities reduce through charts, including truth.
    check({field.name for field in fields(Timestamp)} == {"utime"}, "epoch chart fields")
    check(registry.entails(sem(Timestamp), Time), "Timestamp must entail Time")
    check(registry.entails(sem(TruthBoolean), Truth), "TruthBoolean must entail Truth")
    check(registry.legal(sem(WeatherLimits, PhysicalDomain.AIR)), "weather limits are meaningful")

    # 16. The surviving relations validate their roles.
    window = store.ref("window-1", TaskTimeWindow)
    window.set(TaskTimeWindow(earliest_start=Timestamp(utime=1.0)))
    store.relate(ConstrainedBy, cmd.ref, window)
    authority = store.ref("auth-1", Authority)
    authority.set(Authority(uid=UID(uid="auth-1")))
    store.relate(Holds, authority, uav)
    check(len(store.relations()) >= 3, "facts are queryable")
    try:
        ConstrainedBy(uav, window)
    except TypeError:
        pass
    else:
        raise AssertionError("a vehicle is not directed work")

    # 17. No nominal scaffolding survives; meaning is product, word, or relation.
    for retired in (
        "TaskManeuver",
        "TaskInformation",
        "TaskEffect",
        "TaskTransport",
        "StateChangeCommand",
        "ProcessControlCommand",
        "ConfigurationCommand",
        "MotionCommand",
        "ResourceCommand",
        "MetadataValue",
        "SuccessCriterion",
        "TaskPhase",
    ):
        check(not hasattr(occid2, retired), f"nominal scaffolding {retired} must be gone")
    check(registry.entails(sem(Task), Directive), "a task is directed work")
    check(registry.entails(sem(Command), Directive), "a command is a directive")
    check(registry.entails(sem(Predicate), Condition), "a predicate is a condition")

    print("17 tests passed")


if __name__ == "__main__":
    main()
