"""Protect the actual named codec, including values bare Pydantic JSON loses."""
import json

import pytest
from pydantic import TypeAdapter, ValidationError

from occid import (
    Agent, AltitudeDatum, BooleanLogic, BooleanOperator, CapabilityRole,
    Constraint, Entity, EntityState, GlobalPosition, IdentityBootstrap, IntID,
    LocationState, Node, ObservationTimeBasis, Predicate, Record, StringName,
    Timestamp, UID, is_a,
)
from occid.named import CodecError, Named, dumps, from_data, loads, to_data


def test_every_byte_value_roundtrips_and_uids_remain_atomic():
    for offset in range(256):
        value = UID(bytes((offset + i) % 256 for i in range(16)))
        wire = to_data(value)
        assert wire == {"model": "UID", "value": value.root.hex()}
        assert loads(json.dumps(wire)) == value
    with pytest.raises(ValidationError):
        UID("0" * 16)
    with pytest.raises(CodecError):
        from_data({"model": "UID", "value": "00"})


def test_nested_nominal_type_and_field_presence_survive():
    uid = UID(bytes(range(240, 256)))
    value = Constraint(condition=BooleanLogic(
        operator=BooleanOperator.AND, terms=[Predicate(subject_ref=uid)],
    ))
    restored = loads(dumps(value))
    assert type(restored.condition) is BooleanLogic
    assert type(restored.condition.terms[0]) is Predicate
    assert restored == value
    assert is_a(restored.condition, "Condition")
    assert not isinstance(restored.condition, __import__("occid").Condition)
    assert Constraint().model_fields_set == loads(dumps(Constraint())).model_fields_set
    assert Constraint(condition=None).model_fields_set == loads(dumps(Constraint(condition=None))).model_fields_set
    point = GlobalPosition(lat=36.530440, lon=-83.216383, alt=350, alt_frame=AltitudeDatum.SEA_LEVEL)
    explicit = point.model_copy(update={"datum": "WGS84"})
    assert "datum" not in loads(dumps(point)).model_fields_set
    assert "datum" in loads(dumps(explicit)).model_fields_set
    assert "name" in to_data(AltitudeDatum.SEA_LEVEL)


def test_record_bootstrap_and_complete_state_roundtrip():
    uid = UID(bytes(range(16)))
    now = Timestamp(utime=1788600000.125, tz=0)
    record = Record(uid=UID(bytes(range(240, 256))), id=IntID(2**63 - 1),
                    created_ts=now, updated_ts=now, origin_system="operator", provenance=[])
    state = EntityState(record=record, subject_uid=uid, timestamp=now.utime,
                        position=LocationState(position=None), link_states={},
                        source_observation_ts=now, source_time_basis=ObservationTimeBasis.UNIX)
    restored = loads(dumps(state))
    assert type(restored.record) is Record and type(restored.subject_uid) is UID
    assert restored == state
    assert "received_ts" not in restored.model_fields_set
    assert restored.position.model_fields_set == {"position"}
    assert to_data(record.id)["value"] == {"$integer": str(2**63 - 1)}
    boot = IdentityBootstrap(node_uid=uid, node_id=1, entity_uid=UID(b"e" * 16), entity_id=1,
                             organization_uid=UID(b"o" * 16), organization_id=1)
    assert loads(dumps(boot)) == boot


def test_atomic_enum_flags_maps_bytes_and_text():
    value = {"model": "literal map key", 9: b"\x00\xff", b"key": (1, IntID(2**63)),
             "payload": [StringName("reader"), True, None, CapabilityRole.CONTROLLER | CapabilityRole.RECORDER],
             "text": "nul\x00and surrogate\ud800"}
    assert loads(dumps(value)) == value
    assert loads(dumps({"normal": "map"})) == {"normal": "map"}
    assert loads(dumps(CapabilityRole(0))) == CapabilityRole(0)


@pytest.mark.parametrize("text", [
    '{"model":"UID","model":"IntID","value":2}',
    '{"model":"Missing","value":{}}',
    '{"enum":"AltitudeDatum","name":"MADE_UP"}',
    '{"$bytes":"FF"}', '{"$map":[["x",1],["x",2]]}',
    '{"$integer":"3.0"}', 'NaN', 'Infinity', '9007199254740993',
    '{"model":"Constraint","value":{"condition":{"model":"UID","value":"00000000000000000000000000000000"}}}',
])
def test_bad_inputs_fail_explicitly(text):
    with pytest.raises(CodecError):
        loads(text)


def test_pydantic_boundary_uses_the_same_codec():
    adapter = TypeAdapter(Named[LocationState])
    location = LocationState(position=GlobalPosition(lat=36.530440, lon=-83.216383, alt=300,
                                                     alt_frame=AltitudeDatum.SEA_LEVEL))
    encoded = adapter.dump_json(location)
    assert adapter.validate_json(encoded) == location
    assert json.loads(encoded) == to_data(location)
    with pytest.raises(ValidationError):
        adapter.validate_python(to_data(UID(b"a" * 16)))

