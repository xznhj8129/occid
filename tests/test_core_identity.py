from __future__ import annotations

import unittest

import occid
from pydantic import ValidationError

from occid import (
    Agent,
    AltitudeDatum,
    GlobalPosition,
    Machine,
    Mark,
    Node,
    Organization,
    RecordMeta,
    SensorPayload,
)


ENTITY_UID = bytes.fromhex("6beaac7772304c9eb5780ed9e62355f4")
NODE_UID = bytes.fromhex("0d456ae4fdd34c298c86d9c26fc380e4")
ORG_UID = bytes.fromhex("8538fb17bcf249e4926161ac9e2be633")
LOCATION_UID = bytes.fromhex("a2f5826e0d6749e48ce36415d9f4c01b")
RECORD_UID = bytes.fromhex("c1a7312e46b74b9c8ba78c457e23ab11")


def record() -> RecordMeta:
    return RecordMeta(
        uid=RECORD_UID,
        id=1,
        created_ts=0.0,
        updated_ts=0.0,
        origin_system="test",
        provenance=[],
    )


class CoreIdentityTests(unittest.TestCase):
    def test_entity_concept_is_consumed_but_agent_node_and_organization_keep_identity(self) -> None:
        self.assertNotIn("Entity", occid.__all__)
        entity = Agent(
            record=record(),
            uid=ENTITY_UID,
            id=17,
            node_uids=[NODE_UID],
            name="Mission Agent",
            callsign="FROG-11",
            tags=[],
            metadata={},
            relations=[],
        )
        node = Node(
            uid=NODE_UID,
            id=6,
            entity_uid=ENTITY_UID,
            roles=[],
            addresses=[],
            links={},
            radios={},
            protocols={},
        )
        organization = Organization(
            record=record(),
            uid=ORG_UID,
            id=3,
            name="Example Unit",
            unit_code="EXAMPLE",
            callsign="EXAMPLE-3",
        )

        self.assertEqual(entity.uid.root, ENTITY_UID)
        self.assertEqual(entity.id, 17)
        self.assertEqual([uid.root for uid in entity.node_uids], [NODE_UID])
        self.assertEqual(node.uid.root, NODE_UID)
        self.assertEqual(node.entity_uid.root, ENTITY_UID)
        self.assertEqual(organization.uid.root, ORG_UID)
        self.assertEqual(organization.id, 3)

    def test_record_and_mark_use_uid_identity(self) -> None:
        self.assertNotIn("Location", occid.__all__)
        meta = record()
        mark = Mark(
            record=meta,
            uid=LOCATION_UID,
            id=1,
            name="Sector Bravo",
            position=GlobalPosition(
                lat=36.530440,
                lon=-83.216383,
                alt=0.0,
                alt_frame=AltitudeDatum.RELATIVE,
            ),
        )
        self.assertEqual(meta.uid.root, RECORD_UID)
        self.assertEqual(mark.uid.root, LOCATION_UID)

        with self.assertRaises(ValidationError):
            RecordMeta(
                uid="database-row-1",
                id=1,
                created_ts=0.0,
                updated_ts=0.0,
                origin_system="test",
                provenance=[],
            )

    def test_hardware_serials_are_not_canonical_identity(self) -> None:
        self.assertIn("serial_number", Machine.model_fields)
        self.assertNotIn("sys_id", Machine.model_fields)
        self.assertNotIn("serial_uid", SensorPayload.model_fields)
        self.assertIn("serial_number", SensorPayload.model_fields)

    def test_runtime_entity_representation_rejects_non_uid_identity(self) -> None:
        with self.assertRaises(ValidationError):
            Agent(
                record=record(),
                uid="uav1",
                id=17,
                node_uids=[],
                tags=[],
                metadata={},
                relations=[],
            )


if __name__ == "__main__":
    unittest.main()
