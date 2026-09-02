from __future__ import annotations

import unittest

from pydantic import ValidationError

from occid import IsrObservation, ObservationKind, RecordMeta, VisionDetection


RECORD_UID = bytes.fromhex("371d676ac17a4f37a8de29b58465f8c8")
OBSERVATION_UID = bytes.fromhex("fe21b7f4845840bea224903044423afa")
TRACK_UID = bytes.fromhex("00909d7d8df84363b45e733ff63fc49f")


def record() -> RecordMeta:
    return RecordMeta(
        uid=RECORD_UID,
        id=1,
        created_ts=0.0,
        updated_ts=0.0,
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
            obs_ts=1.0,
            observation_kind=ObservationKind.TRACK,
        )
        self.assertEqual(observation.uid.root, OBSERVATION_UID)
        self.assertEqual(observation.track_uid.root, TRACK_UID)

        with self.assertRaises(ValidationError):
            IsrObservation(
                record=record(),
                uid="observation-1",
                id=1,
                obs_ts=1.0,
            )

    def test_source_detection_tokens_are_refs_not_occid_ids(self) -> None:
        detection = VisionDetection(
            detection_ref="det-17",
            source_frame_ref="frame-2048",
            attributes={},
        )
        self.assertEqual(detection.detection_ref, "det-17")
        self.assertEqual(detection.source_frame_ref, "frame-2048")


if __name__ == "__main__":
    unittest.main()
