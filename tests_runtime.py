"""Revision identity, chart boundaries, and self-describing exchange."""
from copy import deepcopy
from itertools import permutations
from pathlib import Path
import tempfile
import unittest

import msgpack

from occid2 import (
    AmbiguousSemanticMatch, IllegalSemanticCombination, SemanticRegistry,
    Query, UID, decode, new_registry, new_store, sem,
)

POSITION = sem("Position", "Representation.Geodetic")
VALUE = {"lat": 36.530440, "lon": -83.216383, "h": 125.0}


class RuntimeTests(unittest.TestCase):
    def test_explicit_questions_resolve_repeated_observations(self):
        store = new_store()
        target = store.ref("target", "Entity")
        locate = store.task("locate", "TaskIntent.LOCATE").bind("target", target)
        question = Query(POSITION, source="sensor", valid_at=3, observed_before=3, latest=True, provenance={"kind": "observation"})
        self.assertEqual(locate.solve(position=question), {})
        first = target.set(POSITION, VALUE, source="sensor", observed_at=1, validity={"from": 1, "to": 4}, provenance={"kind": "observation"})
        self.assertEqual(locate.solve(position=question)["position"], first)
        second = target.set(POSITION, {**VALUE, "h": 126.0}, source="sensor", observed_at=2, validity={"from": 2, "to": 4}, provenance={"kind": "observation"})
        target.set(POSITION, VALUE, source="other", observed_at=3, validity={"from": 3, "to": 4}, provenance={"kind": "observation"})
        target.set(POSITION, VALUE, source="sensor", observed_at=4, validity={"from": 4, "to": 5}, provenance={"kind": "observation"})
        with self.assertRaises(AmbiguousSemanticMatch):
            locate.solve()
        self.assertEqual(locate.solve(position=question)["position"], second)
        self.assertEqual(target.get(question), second)
        self.assertEqual(target.find(Query(POSITION, source="sensor", valid_at=4, observed_before=3)), [])
        target.set(POSITION, VALUE, source="sensor", observed_at=2, validity={"from": 2, "to": 4}, provenance={"kind": "observation"})
        with self.assertRaises(AmbiguousSemanticMatch):
            locate.solve(position=question)
        with self.assertRaises(KeyError):
            locate.solve(undeclared=question)
        with self.assertRaises(IllegalSemanticCombination):
            locate.solve(position=Query(sem("Mission", "PhysicalDomain.SEA", "Altitude")))

    def test_learned_entailment_queries_original_evidence(self):
        store = new_store()
        target = store.ref("sensor", "Entity")
        datum = target.set("SensorReading", {"native": b"original"}, source="sensor", observed_at=1)
        original = datum.encode()
        locate = store.task("locate", "TaskIntent.LOCATE").bind("target", target)
        self.assertEqual(target.find("Position"), [])
        store.registry.update({"factors": {"SensorReading": {"implies": ["Position"]}}})
        self.assertEqual(target.find("Position"), [datum])
        self.assertEqual(locate.solve()["position"], datum)
        move = store.task("move-learned", "TaskIntent.MOVE")
        with self.assertRaises(TypeError):
            move.bind("destination", datum, interpretation="recorded")
        move.bind("destination", datum)
        self.assertEqual(target.find(Query("Position", interpretation="recorded")), [])
        self.assertNotIn("Position", datum.meaning)
        self.assertIn("Position", store.meaning_of(datum))
        self.assertEqual(datum.encode(), original)
        self.assertEqual(len(target.find()), 1)
        store.registry.update({"factors": {"SensorReading": {}}})
        self.assertEqual(target.find("Position"), [])
        self.assertEqual(datum.encode(), original)

    def test_altitude_reference_is_semantic(self):
        store = new_store()
        subject = store.ref("report")
        ellipsoid = subject.set(POSITION * "AltitudeReference.WGS84Ellipsoid", VALUE)
        msl = subject.set(POSITION * "AltitudeReference.MeanSeaLevel", {**VALUE, "h": 110.0})
        unknown = subject.set(POSITION, VALUE)
        self.assertEqual(subject.find("Position"), [ellipsoid, msl, unknown])
        self.assertEqual(subject.get("Position", "AltitudeReference.WGS84Ellipsoid"), ellipsoid)
        self.assertEqual(subject.get("Position", "AltitudeReference.MeanSeaLevel"), msl)
        with self.assertRaises(IllegalSemanticCombination):
            subject.set(POSITION * "AltitudeReference.WGS84Ellipsoid" * "AltitudeReference.MeanSeaLevel", VALUE)
        self.assertTrue(store.registry.entails(ellipsoid.semantics, POSITION))

    def test_temporal_unknowns_and_incomparable_clocks_are_explicit(self):
        store = new_store()
        target = store.ref("sensor")
        target.set(POSITION, VALUE, source="sensor", observed_at="2026-10-11T12:00:00Z")
        tie = target.set(POSITION, VALUE, source="sensor", observed_at="2026-10-11T08:00:00-04:00")
        target.set("Velocity", {"native": 2}, source="sensor", observed_at=123)
        self.assertEqual(len(target.find(Query(POSITION, latest=True))), 2)
        with self.assertRaises(AmbiguousSemanticMatch):
            target.get(Query(POSITION, latest=True))
        self.assertEqual(target.find(Query(POSITION, valid_at="2026-10-11T12:00:00Z")), [])
        missing = target.set(POSITION, VALUE, source="sensor")
        with self.assertRaises(AmbiguousSemanticMatch):
            target.get(Query(POSITION, latest=True))
        self.assertEqual(target.find(Query(POSITION, observed_before="2026-10-11T12:00:00Z"))[-1], tie)
        self.assertIn(missing, target.find(POSITION))
        for timestamp in (True, float("nan"), "2026-10-11T12:00:00"):
            with self.subTest(timestamp=timestamp), self.assertRaises(ValueError):
                Query(observed_before=timestamp)
        other = store.ref("other")
        other.set(POSITION, VALUE, source="one", observed_at=1)
        other.set(POSITION, VALUE, source="two", observed_at=2)
        with self.assertRaises(AmbiguousSemanticMatch):
            other.get(Query(POSITION, latest=True))
        other.set(POSITION, VALUE, source="one", observed_at="2026-10-11T12:00:00Z")
        with self.assertRaises(AmbiguousSemanticMatch):
            other.get(Query(POSITION, source="one", latest=True))

    def test_model_refinement_exposes_conflicts_without_rewriting_evidence(self):
        store = new_store(registry=SemanticRegistry({"factors": {"Reading": {}}, "axes": {"Reference": {"cardinality": "many", "values": ["A", "B"]}}}))
        target = store.ref("sensor")
        datum = target.set(sem("Reading", "Reference.A", "Reference.B"), {"native": 12})
        wire = datum.encode()
        store.registry.update({"axes": {"Reference": {"cardinality": "one", "values": ["A", "B"]}}})
        with self.assertRaises(IllegalSemanticCombination):
            target.find("Reading")
        self.assertEqual(target.get(Query("Reading", interpretation="recorded")), datum)
        self.assertEqual(datum.encode(), wire)

    def test_wire_definition_identity_is_resolvable_and_revisions_are_immutable(self):
        store = new_store()
        target = store.ref("sensor")
        datum = target.set(POSITION, VALUE)
        payload = datum.encode(include_definitions=False)
        self.assertNotIn("definitions", msgpack.unpackb(payload, raw=False))
        self.assertEqual(decode(payload, registry=store.registry), datum)
        with self.assertRaises(ValueError):
            decode(payload)
        revision = store.registry.at(datum.definition_id)
        with self.assertRaises(ValueError):
            revision.update({"factors": {"Changed": {}}})
        store.registry.update({"factors": {"NewMeaning": {}}})
        self.assertEqual(decode(payload, registry=store.registry), datum)
        self.assertNotIn("NewMeaning", datum.definitions["factors"])
        envelope = msgpack.unpackb(payload, raw=False)
        envelope["native_extension"] = {"raw": b"original"}
        extended = decode(msgpack.packb(envelope, use_bin_type=True), registry=store.registry)
        self.assertEqual(decode(extended.encode(include_definitions=False), registry=store.registry).extensions, extended.extensions)
        self.assertLess(len(payload), len(datum.encode()))

    def test_in_memory_evidence_does_not_require_wire_serialization(self):
        store = new_store()
        target = store.ref("sensor")
        datum = target.set("Unresolved", {"native": complex(1, 2)})
        self.assertEqual(target.get("Unresolved").value, {"native": complex(1, 2)})
        with self.assertRaises(TypeError):
            datum.encode()
        receiver = new_store()
        self.assertEqual(receiver.add(datum), datum)

    def test_subject_identity_and_additive_assertions(self):
        uid = UID.new()
        self.assertEqual(len(uid), 16)
        self.assertEqual(uid, UID(bytes(uid)))
        for invalid in ("uav-1", b"short", bytes(17)):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                UID(invalid)
        store = new_store()
        person = store.ref(uid, "Person")
        with self.assertRaises(IllegalSemanticCombination):
            store.ref(uid, "Machine")
        self.assertTrue(store.registry.entails(person.semantics, "Person"))
        self.assertEqual(person.set("Unknown.Property", {"uid": "external-name"}).value["uid"], "external-name")
        for invalid in ("", b"short", 1):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                store.ref(invalid)

    def test_product_laws_and_constraint_derivation(self):
        registry = new_registry()
        terms = ("UnmannedVehicle", "PhysicalDomain.AIR", "Airframe.MULTIROTOR")
        for ordering in permutations(terms):
            product = sem(*ordering, ordering[0])
            self.assertTrue(registry.equivalent(product, registry.product("Drone")))
            self.assertTrue(registry.entails(product, "Machine"))
            self.assertFalse(registry.legal(product * "BloodGroup.A_POS"))
        registry.update({"axes": {"Access": {"cardinality": "one", "values": {"Restricted": {"requires": ["Authority"]}, "Public": {}}}}})
        self.assertTrue(registry.entails(sem("Access.Restricted"), "Authority"))
        self.assertFalse(registry.legal(sem("Access.Restricted", "Access.Public")))

    def test_chart_validation_preserves_unknown_fields_and_raw_values(self):
        store = new_store()
        uav = store.ref("uav-1")
        for bad in ("36.5", True, float("nan"), float("inf")):
            with self.subTest(latitude=bad), self.assertRaises(TypeError):
                uav.set(POSITION, {**VALUE, "lat": bad})
        with self.assertRaises(ValueError):
            uav.set(POSITION, {"lat": 36.530440})
        self.assertEqual(uav.find(), [])
        value = {**VALUE, "unknown": b"\x00\xff", "explicit_null": None, "large_native_count": 2**63}
        datum = uav.set(POSITION, value, source={"raw": b"native"}, provenance={"uncertainty": {"h": 3.0}}, validity={"until": "2026-10-11T00:00:00Z"})
        value["h"] = 999
        returned = datum.value
        returned["h"] = -1
        self.assertEqual(datum.value["h"], 125.0)
        self.assertEqual(decode(datum.encode()), datum)
        self.assertNotIn("missing", datum.value)
        self.assertIsNone(datum.value["explicit_null"])
        self.assertEqual(datum.value["unknown"], b"\x00\xff")

    def test_wire_can_resolve_definitions_without_the_sender_package(self):
        registry = SemanticRegistry({"factors": {"NovelQuantity": {}}, "charts": {"NovelQuantity": {"coords": {"reading": "float[widgets]"}, "context": {"reference": "sender-reference"}}}})
        datum = new_store(registry=registry).ref("sensor").set("NovelQuantity", {"reading": 12.0, "native": {"extra": None}})
        restored = decode(datum.encode())
        self.assertEqual(restored, datum)
        receiver_registry = SemanticRegistry(restored.definitions)
        self.assertEqual(receiver_registry.coordinates(restored.semantics)["reading"].unit, "widgets")
        self.assertEqual(receiver_registry.charts[0].context, {"reference": "sender-reference"})
        envelope = msgpack.unpackb(datum.encode(), raw=False)
        envelope["future_envelope_field"] = {"opaque": b"\xff"}
        extended = decode(msgpack.packb(envelope, use_bin_type=True))
        self.assertEqual(decode(extended.encode()).extensions, {"future_envelope_field": {"opaque": b"\xff"}})

    def test_reject_malformed_wire_and_duplicate_fields(self):
        datum = new_store().ref("sensor").set(POSITION, VALUE)
        valid = msgpack.unpackb(datum.encode(), raw=False)
        for field, bad in (("format", "other"), ("definition_id", "wrong"), ("meaning", []), ("semantics", [True]), ("subject", b"short"), ("provenance", [])):
            envelope = {**valid, field: bad}
            with self.subTest(field=field), self.assertRaises((ValueError, TypeError)):
                decode(msgpack.packb(envelope, use_bin_type=True))
        for envelope in ({}, [1, {}], {**valid, "value": {"lat": "bad", "lon": 0.0, "h": 0.0}}):
            with self.assertRaises((ValueError, TypeError)):
                decode(msgpack.packb(envelope, use_bin_type=True))
        with self.assertRaisesRegex(ValueError, "duplicate wire key"):
            decode(bytes.fromhex("82a17801a17802"))

    def test_invalid_definition_updates_are_atomic(self):
        store = new_store()
        registry = store.registry
        subject = store.ref("uav", "UAV")
        before = subject.set(POSITION, VALUE)
        initial_spec = registry.spec
        initial_id = registry.definition_id
        invalid_updates = (
            {"aliases": {"CycleA": ["CycleB"], "CycleB": ["CycleA"]}},
            {"factors": {"Impossible": {"implies": ["Machine", "Biological"]}}},
            {"factors": {"Typo": {"requiers": ["Machine"]}}},
            {"axes": {"Invalid": {"cardinality": "sometimes", "values": ["A"]}}},
            {"expressions": {"Broken": {"of": "Missing"}}},
            {"expressions": {"Broken": {"factors": ["Task"], "given": {"actor": "Entity"}, "equations": ["Position(actor) = undeclared"]}}},
            {"expressions": {"Broken": {"factors": ["Task"], "given": {"actor": "Entity"}, "sought": {"answer": "Velocity"}, "equations": ["Position(actor) = answer"]}}},
            {"relations": {"Invalid": {"specializes": "AssignedWork", "operands": {"assignee": "Root", "work": "Task"}}}},
            {"charts": {"Position * Representation.Geodetic": {"lat": "unknown[deg]"}}},
            {"mappings": {"bad": {"semantics": ["Undeclared"]}}},
        )
        for update in invalid_updates:
            with self.subTest(update=update), self.assertRaises(ValueError):
                registry.update(update)
            self.assertEqual(registry.spec, initial_spec)
            self.assertEqual(registry.definition_id, initial_id)
            self.assertEqual(subject.get(POSITION), before)
        copied = registry.spec
        copied["aliases"]["Drone"] = ["Person"]
        self.assertTrue(registry.entails(registry.product("Drone"), "Machine"))

    def test_duplicate_yaml_and_malformed_rule(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "definitions.yaml"
            path.write_text("version: 2\nversion: 2\n")
            with self.assertRaisesRegex(ValueError, "duplicate YAML key"):
                SemanticRegistry.load(path)
        with self.assertRaises(ValueError):
            SemanticRegistry({"factors": {"A": {"applies": {"all": [], "not": "A"}}}})

    def test_repeated_observations_stay_ambiguous_even_with_equal_values(self):
        store = new_store()
        subject = store.ref("uav")
        first = subject.set(POSITION, VALUE, source="sensor-1", observed_at=1)
        second = subject.set(POSITION, VALUE, source="sensor-2", observed_at=2)
        self.assertNotEqual(first.id, second.id)
        self.assertEqual(subject.find("GlobalPosition"), [first, second])
        with self.assertRaises(AmbiguousSemanticMatch):
            subject.get("GlobalPosition")
        task = store.task("locate", "TaskIntent.LOCATE")
        target = store.ref("uav", "Entity")
        task.bind("target", target)
        with self.assertRaises(AmbiguousSemanticMatch):
            task.solve()
        empty = store.ref("empty", "Entity")
        self.assertEqual(empty.find(POSITION), [])
        with self.assertRaises(KeyError):
            empty.get(POSITION)
        with self.assertRaises(IllegalSemanticCombination):
            empty.find("Altitude", "PhysicalDomain.SEA")

    def test_live_axes_charts_constraints_aliases_and_word_mappings(self):
        store = new_store()
        registry = store.registry
        axis = registry.axis("Representation")
        axis_spec = deepcopy(registry.spec["axes"]["Representation"])
        axis_spec["values"].append("SensorNative")
        registry.update({
            "axes": {"Representation": axis_spec},
            "factors": {"SensorPosition": {"implies": ["Position"]}},
            "aliases": {"NativeFix": ["SensorPosition", "Representation.SensorNative"]},
            "charts": {"SensorPosition * Representation.SensorNative": {"native": "bytes"}},
            "expressions": {"FIND_SENSOR": {"factors": ["Task", "Realm.INFORMATION"], "given": {"sensor": "Entity"}, "sought": {"fix": "Position"}, "equations": ["Position(sensor) = fix"], "words": {"SensorWord.FIND": ["TemporalMode.ACHIEVE"]}}},
        })
        sensor = store.ref("sensor", "Entity")
        expression = store.task("find", "SensorWord.FIND").bind("sensor", sensor)
        self.assertEqual(expression.solve(), {})
        datum = sensor.set("NativeFix", {"native": b"original sensor format"})
        self.assertEqual(axis.SensorNative.name, "Representation.SensorNative")
        self.assertEqual(sensor.find("Position"), [datum])
        self.assertEqual(expression.solve()["fix"], datum)

    def test_mapping_revision_and_definition_changes_preserve_history(self):
        store = new_store()
        registry = store.registry
        registry.update({"factors": {"Unresolved": {}}, "mappings": {"report": {"semantics": ["Unresolved"]}}})
        subject = store.ref("source-subject")
        original = subject.set(sem(), {"native": b"\x00\xff", "explicit_null": None, "height_a": 125.0, "height_b": 110.0}, source="native report", observed_at=123, validity={"from": 123, "to": 124})
        old = store.interpret(original, "report")
        old_wire = old.encode()
        registry.update({"factors": {"Unresolved": {"implies": ["Position"]}}, "mappings": {"report": {"semantics": ["Unresolved"], "context": {"reference": "revised semantic association"}}}})
        new = store.interpret(original, "report")
        self.assertEqual(subject.find("Position"), [old, new])
        self.assertEqual(subject.find(Query("Position", interpretation="recorded")), [new])
        self.assertEqual(old.encode(), old_wire)
        self.assertEqual(old.value, new.value)
        self.assertEqual(old.provenance["derived_from"], [original.id])
        self.assertNotEqual(old.definition_id, new.definition_id)
        self.assertEqual(subject.find()[0], original)
        self.assertEqual(decode(old_wire), old)
        self.assertNotIn("Position", registry.at(old.definition_id).closure(sem("Unresolved")))

    def test_bindings_relation_order_units_and_metadata(self):
        store = new_store()
        actor = store.ref("uav", "UAV")
        target = store.ref(UID.new(), "Entity")
        fact = target.set(POSITION, {**VALUE, "source_extension": {"native": b"\x01"}}, source={"sensor": 5}, observed_at="2026-10-11T00:00:00Z", provenance={"kind": "observation", "frame": "WGS84 ellipsoid", "uncertainty": 0.5})
        locate = store.task("locate", "TaskIntent.LOCATE").bind("target", target)
        move = store.task("move", "TaskIntent.MOVE").bind("actor", actor).bind("destination", fact)
        relation = store.relate("AssignedWork", work=move.ref, assignee=actor)
        with self.assertRaises(TypeError):
            store.relate("AssignedWork", move.ref, actor)
        self.assertEqual(store.ref(target.uid).get(POSITION), fact)
        self.assertEqual(store.expression("locate").solve()["position"], fact)
        self.assertEqual(store.expression("move").unbound, [])
        self.assertEqual(store.expression("move").bindings["destination"], fact)
        link = store.relations("Directed")[0]
        self.assertEqual(link.id, relation.id)
        self.assertEqual(tuple(link.roles), ("assignee", "work"))
        self.assertEqual(tuple(ref.uid for ref in link.operands), ("uav", "move"))
        self.assertEqual(store.registry.at(fact.definition_id).coordinates(POSITION)["lat"].unit, "deg")

    def test_import_retains_sender_meaning_without_activating_its_definitions(self):
        sender = new_store(registry=SemanticRegistry({"factors": {"ForeignReading": {}}, "charts": {"ForeignReading": {"reading": "float[foreign-unit]"}}}))
        sent = sender.ref("foreign-sensor").set("ForeignReading", {"reading": 12.5, "unknown": None}, source="sender", observed_at=12)
        receiver = new_store()
        active_id = receiver.registry.definition_id
        received = receiver.add(decode(sent.encode()))
        self.assertEqual(received, sent)
        self.assertEqual(receiver.ref("foreign-sensor").get("ForeignReading"), sent)
        self.assertEqual(receiver.add(decode(sent.encode())), received)
        self.assertEqual(len(receiver.ref("foreign-sensor").find()), 1)
        self.assertEqual(receiver.registry.definition_id, active_id)
        self.assertEqual(receiver.registry.at(sent.definition_id).coordinates(sent.semantics)["reading"].unit, "foreign-unit")
        envelope = msgpack.unpackb(sent.encode(), raw=False)
        envelope["value"]["reading"] = 13.5
        with self.assertRaises(ValueError):
            receiver.add(decode(msgpack.packb(envelope, use_bin_type=True)))

    def test_revision_access(self):
        store = new_store()
        registry = store.registry
        task = store.task("move", "TaskIntent.MOVE")
        self.assertEqual(registry.product("TaskIntent.MOVE"), task.factors)
        old_id = registry.definition_id
        registry.update({"factors": {"NewMeaning": {}}})
        self.assertEqual(registry.at(old_id).product("TaskIntent.MOVE"), task.factors)
        with self.assertRaises(TypeError):
            registry.aliases["Drone"] = ("Person",)
        with self.assertRaises(TypeError):
            task.expression.given["actor"] = sem("Person")


if __name__ == "__main__":
    unittest.main()
