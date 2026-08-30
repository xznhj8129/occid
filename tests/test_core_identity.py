from __future__ import annotations

import unittest

from pydantic import ValidationError

from occid import Entity, Location, Machine, Node, Organization, RecordMeta, SensorPayload


ENTITY_UID = "6beaac77-7230-4c9e-b578-0ed9e62355f4"
NODE_UID = "0d456ae4-fdd3-4c29-8c86-d9c26fc380e4"
ORG_UID = "8538fb17-bcf2-49e4-9261-61ac9e2be633"
LOCATION_UID = "a2f5826e-0d67-49e4-8ce3-6415d9f4c01b"
RECORD_UID = "c1a7312e-46b7-4b9c-8ba7-8c457e23ab11"


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
    def test_entity_node_and_organization_use_uid_identity(self) -> None:
        entity = Entity(
            record=record(),
            uid=ENTITY_UID,
            id=17,
            node_uids=[NODE_UID],
            name="Frog UAV 1",
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

        self.assertEqual(str(entity.uid), ENTITY_UID)
        self.assertEqual(entity.id, 17)
        self.assertEqual([str(uid) for uid in entity.node_uids], [NODE_UID])
        self.assertEqual(str(node.uid), NODE_UID)
        self.assertEqual(str(node.entity_uid), ENTITY_UID)
        self.assertEqual(str(organization.uid), ORG_UID)
        self.assertEqual(organization.id, 3)

    def test_record_and_location_use_uid_identity(self) -> None:
        meta = record()
        location = Location(record=meta, uid=LOCATION_UID, id=1, name="Sector Bravo")
        self.assertEqual(str(meta.uid), RECORD_UID)
        self.assertEqual(str(location.uid), LOCATION_UID)

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
        self.assertNotIn("sys_id", Machine.model_fields)
        self.assertIn("serial_number", Machine.model_fields)
        self.assertNotIn("serial_uid", SensorPayload.model_fields)
        self.assertIn("serial_number", SensorPayload.model_fields)

    def test_entity_rejects_non_uid_identity(self) -> None:
        with self.assertRaises(ValidationError):
            Entity(
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
