from __future__ import annotations

import unittest

import occid
from occid import (
    Activation,
    ActivationPhase,
    BooleanLogic,
    BooleanOperator,
    Capability,
    Condition,
    Constraint,
    Cue,
    Data,
    FlightControlState,
    GNC,
    Health,
    IdentifierType,
    Object,
    OCCID_SCHEMA_VERSION,
    Payload,
    PlanContingency,
    Predicate,
    Property,
    State,
    StringID,
    Task,
    Validation,
    ValidationStatus,
)


def sid(value: str) -> StringID:
    return StringID(id_type=IdentifierType.DB_ID, value=value)


class ApexPrimitiveTests(unittest.TestCase):
    def test_capability_is_an_object_property(self) -> None:
        self.assertTrue(issubclass(Capability, Property))
        self.assertIn("capabilities", Object.model_fields)
        payload = Payload(capabilities=[Capability()])
        self.assertEqual(Payload.decode(payload.encode()), payload)

    def test_condition_is_predicate_logic_not_state(self) -> None:
        self.assertTrue(issubclass(Condition, Data))
        self.assertFalse(issubclass(Condition, State))
        self.assertTrue(issubclass(Health, State))
        predicate = Predicate(subject_ref=sid("payload.1"))
        condition = BooleanLogic(operator=BooleanOperator.NOT, terms=[predicate])
        constraint = Constraint(condition=condition)
        self.assertEqual(constraint.condition, condition)
        self.assertNotIn("ConstraintCondition", occid.__all__)
        for old_name in ("Conjunction", "Disjunction", "Negation"):
            self.assertNotIn(old_name, occid.__all__)

    def test_boolean_logic_uses_one_closed_operator_axis(self) -> None:
        first = Predicate(subject_ref=sid("payload.1"))
        second = Predicate(subject_ref=sid("payload.2"))
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
        predicate = Predicate(subject_ref=sid("payload.1"))
        validation = Validation(condition=predicate, status=ValidationStatus.VALID, updated_ts=1.0)
        self.assertEqual(Validation.decode(validation.encode()), validation)
        self.assertIn("preconditions", Task.model_fields)
        contingency = PlanContingency(
            contingency_id=sid("contingency.1"),
            condition=predicate,
            response="continue",
            task_ids=[],
        )
        self.assertEqual(contingency.condition, predicate)

    def test_activation_and_cue_are_protocol_neutral_state(self) -> None:
        activation = Activation(
            phase=ActivationPhase.READY,
            remaining_uses=2,
        )
        cue = Cue(
            source_id=sid("payload.1"),
            target_id=sid("target.1"),
            distance_m=25.0,
            label="target",
        )
        self.assertTrue(issubclass(Activation, State))
        self.assertTrue(issubclass(Cue, State))
        self.assertIsNone(cue.bearing_rad)
        self.assertIsNone(cue.elevation_rad)
        self.assertEqual(Activation.decode(activation.encode()), activation)
        self.assertEqual(Cue.decode(cue.encode()), cue)

    def test_gnc_is_distinct_from_cueing(self) -> None:
        self.assertTrue(issubclass(GNC, State))
        self.assertTrue(issubclass(FlightControlState, GNC))
        self.assertFalse(issubclass(Cue, GNC))
        self.assertNotIn("Guidance", occid.__all__)
        self.assertEqual(OCCID_SCHEMA_VERSION, (5, 2, 0))


if __name__ == "__main__":
    unittest.main()
