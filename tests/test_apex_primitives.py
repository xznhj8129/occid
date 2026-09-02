from __future__ import annotations

import unittest

import occid
from occid import (
    Activation,
    ActivationPhase,
    BooleanLogic,
    BooleanOperator,
    Capability,
    Constraint,
    Cue,
    FlightControlState,
    GNC,
    Health,
    Payload,
    PlanContingency,
    Predicate,
    Task,
    Validation,
    ValidationStatus,
)


PAYLOAD_UID_1 = bytes.fromhex("030ad7ef905a4ce7a97b8e0d44d3e138")
PAYLOAD_UID_2 = bytes.fromhex("e512918a26e04b239931c5e4fe24da4e")
TARGET_UID = bytes.fromhex("a55c2fe08e0642f3a50f1324cc1f9266")


class ApexPrimitiveTests(unittest.TestCase):
    def test_capability_is_a_runtime_type_and_payload_representation(self) -> None:
        self.assertEqual(Capability.__occid_semantic_role__, "type")
        self.assertEqual(Payload.__occid_semantic_role__, "representation")
        self.assertNotIn("Object", occid.__all__)
        self.assertNotIn("Property", occid.__all__)
        self.assertIn("capabilities", Payload.model_fields)
        payload = Payload(capabilities=[Capability()])
        self.assertEqual(Payload.decode(payload.encode()), payload)

    def test_condition_logic_compiles_into_constraint_without_runtime_ontology(self) -> None:
        for concept in ("Condition", "Data", "State"):
            self.assertNotIn(concept, occid.__all__)
        self.assertEqual(Health.__occid_semantic_role__, "type")
        predicate = Predicate(subject_ref=PAYLOAD_UID_1)
        condition = BooleanLogic(operator=BooleanOperator.NOT, terms=[predicate])
        constraint = Constraint(condition=condition)
        self.assertEqual(constraint.condition, condition)
        self.assertNotIn("ConstraintCondition", occid.__all__)
        for old_name in ("Conjunction", "Disjunction", "Negation"):
            self.assertNotIn(old_name, occid.__all__)

    def test_boolean_logic_uses_one_closed_operator_axis(self) -> None:
        first = Predicate(subject_ref=PAYLOAD_UID_1)
        second = Predicate(subject_ref=PAYLOAD_UID_2)
        condition = BooleanLogic(operator=BooleanOperator.NOR, terms=[first, second])
        self.assertEqual(BooleanLogic.decode(condition.encode()), condition)
        self.assertEqual(
            set(BooleanOperator),
            {
                BooleanOperator.NONE,
                BooleanOperator.NOT,
                BooleanOperator.AND,
                BooleanOperator.OR,
                BooleanOperator.XOR,
                BooleanOperator.NAND,
                BooleanOperator.NOR,
                BooleanOperator.XNOR,
            },
        )

    def test_condition_validation_is_separate_runtime_state(self) -> None:
        predicate = Predicate(subject_ref=PAYLOAD_UID_1)
        validation = Validation(condition=predicate, status=ValidationStatus.VALID, updated_ts=1.0)
        self.assertEqual(Validation.decode(validation.encode()), validation)
        self.assertIn("preconditions", Task.model_fields)
        contingency = PlanContingency(
            id=1,
            condition=predicate,
            response="continue",
            task_uids=[],
        )
        self.assertEqual(contingency.condition, predicate)

    def test_activation_and_cue_are_protocol_neutral_types(self) -> None:
        activation = Activation(
            phase=ActivationPhase.READY,
            remaining_uses=2,
        )
        cue = Cue(
            source_uid=PAYLOAD_UID_1,
            target_uid=TARGET_UID,
            distance_m=25.0,
            label="target",
        )
        self.assertEqual(Activation.__occid_semantic_role__, "type")
        self.assertEqual(Cue.__occid_semantic_role__, "type")
        self.assertIsNone(cue.bearing_rad)
        self.assertIsNone(cue.elevation_rad)
        self.assertEqual(Activation.decode(activation.encode()), activation)
        self.assertEqual(Cue.decode(cue.encode()), cue)

    def test_gnc_representation_is_flat(self) -> None:
        self.assertEqual(GNC.__occid_semantic_role__, "type")
        self.assertEqual(FlightControlState.__occid_semantic_role__, "representation")
        self.assertEqual(Cue.__occid_semantic_role__, "type")
        self.assertNotIn("Guidance", occid.__all__)
        self.assertNotIn("OCCID_SCHEMA_VERSION", occid.__all__)


if __name__ == "__main__":
    unittest.main()
