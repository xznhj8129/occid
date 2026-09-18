from __future__ import annotations

import unittest

from pydantic import ValidationError

from occid import (
    IntID,
    IsrObservation,
    ObservationKind,
    Record,
    Timestamp,
    VisionDetection,
)


RECORD_UID = bytes.fromhex("371d676ac17a4f37a8de29b58465f8c8")
OBSERVATION_UID = bytes.fromhex("fe21b7f4845840bea224903044423afa")
TRACK_UID = bytes.fromhex("00909d7d8df84363b45e733ff63fc49f")


def record() -> Record:
    return Record(
        uid=RECORD_UID,
        id=1,
        created_ts=Timestamp(utime=0.0, tz=0),
        updated_ts=Timestamp(utime=0.0, tz=0),
        origin_system="test",
        provenance=[],
    )


class ObservationIdentityTests(unittest.TestCase):
    def test_observation_and_track_use_uid(self) -> None:
        observation = IsrObservation(
            record=record(),
            uid=OBSERVATION_UID,
            id=1,
            track_uid=TRACK_UID,
            evidence_media_uids=[],
            obs_ts=Timestamp(utime=1.0, tz=0),
            observation_kind=ObservationKind.TRACK,
        )
        self.assertEqual(observation.uid.root, OBSERVATION_UID)
        self.assertEqual(observation.track_uid.root, TRACK_UID)

        with self.assertRaises(ValidationError):
            IsrObservation(
                record=record(),
                uid="observation-1",
                id=1,
                evidence_media_uids=[],
                obs_ts=Timestamp(utime=1.0, tz=0),
            )

    def test_detection_identity_is_namespaced_integer_not_string(self) -> None:
        detection = VisionDetection(detection_id=17, attributes={})
        self.assertIsInstance(detection.detection_id, IntID)
        self.assertEqual(detection.detection_id.root, 17)

        with self.assertRaises(ValidationError):
            VisionDetection(detection_id="det-17", attributes={})


if __name__ == "__main__":
    unittest.main()
