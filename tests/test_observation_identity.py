from __future__ import annotations

import unittest

from pydantic import ValidationError

from occid import IsrObservation, ObservationKind, RecordMeta, VisionDetection


RECORD_UID = "371d676a-c17a-4f37-a8de-29b58465f8c8"
OBSERVATION_UID = "fe21b7f4-8458-40be-a224-903044423afa"
TRACK_UID = "00909d7d-8df8-4363-b45e-733ff63fc49f"


def record() -> RecordMeta:
    return RecordMeta(
        record_id=RECORD_UID,
        created_ts=0.0,
        updated_ts=0.0,
        origin_system="test",
        provenance=[],
    )


class ObservationIdentityTests(unittest.TestCase):
    def test_observation_and_track_use_uid(self) -> None:
        observation = IsrObservation(
            record=record(),
            obs_id=OBSERVATION_UID,
            track_id=TRACK_UID,
            obs_ts=1.0,
            observation_kind=ObservationKind.TRACK,
        )
        self.assertEqual(observation.obs_id, OBSERVATION_UID)
        self.assertEqual(observation.track_id, TRACK_UID)

        with self.assertRaises(ValidationError):
            IsrObservation(
                record=record(),
                obs_id="observation-1",
                obs_ts=1.0,
            )

    def test_source_detection_ids_remain_local_strings(self) -> None:
        detection = VisionDetection(
            detection_id="det-17",
            source_frame_id="frame-2048",
            attributes={},
        )
        self.assertEqual(detection.detection_id, "det-17")
        self.assertEqual(detection.source_frame_id, "frame-2048")


if __name__ == "__main__":
    unittest.main()
