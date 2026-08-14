from __future__ import annotations

import unittest
from pathlib import Path

import yaml

import occid
from occid import (
    AltitudeDatum,
    Assignment,
    Authority,
    Command,
    Communication,
    ConfigurationCommand,
    Control,
    ControlLease,
    Directive,
    Execution,
    ExecutionCommand,
    GlobalPosition,
    IdentifierType,
    Interface,
    MotionCommand,
    MotionOperation,
    OCCID_MODEL_ID_BY_CLASS,
    ProcessControlCommand,
    RecordMeta,
    ResourceCommand,
    State,
    StateChangeCommand,
    StringID,
    Task,
    TaskIntent,
    TaskType,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def sid(value: str) -> StringID:
    return StringID(id_type=IdentifierType.DB_ID, value=value)


def record_meta(value: str) -> RecordMeta:
    return RecordMeta(
        record_id=sid(value),
        created_ts=1.0,
        updated_ts=1.0,
        origin_system="occid.tests",
        provenance=[],
    )


def task(**overrides) -> Task:
    values = dict(
        record=record_meta("record.task.1"),
        task_id=sid("task.1"),
        instruction="Search Route 6 and establish what vehicle traffic is using it.",
        task_type=TaskType.INFORMATION,
        task_intent=TaskIntent.SEARCH,
        target_refs=[],
        location_refs=[sid("location.route6")],
        constraints=[],
    )
    values.update(overrides)
    return Task(**values)


class ControlRefactorTests(unittest.TestCase):
    def test_control_hierarchy_matches_locked_refactor(self) -> None:
        self.assertTrue(issubclass(Directive, Control))
        self.assertTrue(issubclass(Task, Directive))
        self.assertTrue(issubclass(Command, Directive))
        for family in (
            StateChangeCommand,
            ProcessControlCommand,
            ConfigurationCommand,
            MotionCommand,
            ResourceCommand,
            ExecutionCommand,
        ):
            self.assertTrue(issubclass(family, Command))

        self.assertTrue(issubclass(Authority, Control))
        self.assertTrue(issubclass(Assignment, Control))
        self.assertFalse(issubclass(Assignment, State))
        self.assertTrue(issubclass(Execution, State))

    def test_task_is_one_generic_instruction_bearing_model(self) -> None:
        value = task()
        self.assertEqual(value.task_type, TaskType.INFORMATION)
        self.assertEqual(value.task_intent, TaskIntent.SEARCH)
        self.assertEqual(value.instruction, "Search Route 6 and establish what vehicle traffic is using it.")
        self.assertEqual(value.location_refs, [sid("location.route6")])
        self.assertIsNone(value.objective_id)

        decoded = Task.decode(value.encode())
        self.assertEqual(decoded, value)
        self.assertEqual(decoded.instruction, value.instruction)
        self.assertEqual(decoded.target_refs, value.target_refs)
        self.assertEqual(decoded.location_refs, value.location_refs)

    def test_task_rejects_invalid_type_intent_pairs(self) -> None:
        with self.assertRaisesRegex(ValueError, "not valid for task_type"):
            task(task_type=TaskType.MANEUVER, task_intent=TaskIntent.SEARCH)
        with self.assertRaisesRegex(ValueError, "not valid for task_type"):
            task(task_type=TaskType.TRANSPORT, task_intent=TaskIntent.HOLD)

    def test_task_accepts_all_declared_intent_families(self) -> None:
        accepted = (
            (TaskType.MANEUVER, TaskIntent.MOVE),
            (TaskType.EFFECT, TaskIntent.PROTECT),
            (TaskType.INFORMATION, TaskIntent.ASSESS),
            (TaskType.TRANSPORT, TaskIntent.EVACUATE),
        )
        for task_type, task_intent in accepted:
            with self.subTest(task_type=task_type, task_intent=task_intent):
                self.assertEqual(task(task_type=task_type, task_intent=task_intent).task_intent, task_intent)

    def test_assignment_references_first_class_authority(self) -> None:
        self.assertIn("authority_id", Assignment.model_fields)
        self.assertNotIn("authority", Assignment.model_fields)
        self.assertTrue(issubclass(ControlLease, Authority))

    def test_interface_is_communication_not_control(self) -> None:
        self.assertTrue(issubclass(Interface, Communication))
        self.assertFalse(issubclass(Interface, Control))

    def test_motion_command_is_semantic_and_endpoint_neutral(self) -> None:
        command = MotionCommand(
            target_ref=sid("entity.uav.7"),
            constraints=[],
            operation=MotionOperation.MOVE_TO,
            destination=GlobalPosition(
                lat=45.5017,
                lon=-73.5673,
                alt=120.0,
                alt_frame=AltitudeDatum.RELATIVE,
            ),
            yaw_rad=1.25,
        )
        self.assertEqual(MotionCommand.decode(command.encode()), command)
        self.assertEqual(command.operation, MotionOperation.MOVE_TO)

    def test_removed_ontology_classes_are_not_runtime_aliases(self) -> None:
        removed = (
            "Mission",
            "IsrTask",
            "MoveTask",
            "HoldTask",
            "ResupplyTask",
            "Reference",
            "Mark",
            "ReferencePath",
            "Region",
            "Boundary",
            "FlightCommand",
            "ArmCommand",
            "DisarmCommand",
            "GoToCommand",
            "SetModeCommand",
            "TaskCommand",
            "ApplyPlanCommand",
            "CombatTask",
            "TaskAssignment",
            "ExecutionStatusRequest",
        )
        for name in removed:
            with self.subTest(name=name):
                self.assertFalse(hasattr(occid, name), name)

    def test_source_layout_matches_semantic_placement(self) -> None:
        self.assertTrue((REPO_ROOT / "lib/schema/core/control/assignment.schema.yaml").is_file())
        self.assertTrue((REPO_ROOT / "lib/schema/core/control/authority.schema.yaml").is_file())
        self.assertTrue((REPO_ROOT / "lib/schema/core/control/directive.schema.yaml").is_file())
        self.assertTrue((REPO_ROOT / "lib/schema/core/communication/interface.schema.yaml").is_file())
        self.assertTrue((REPO_ROOT / "lib/schema/core/data/state/execution.schema.yaml").is_file())
        self.assertFalse((REPO_ROOT / "lib/schema/core/control/reference.schema.yaml").exists())
        self.assertFalse((REPO_ROOT / "lib/schema/core/control/interface.schema.yaml").exists())
        self.assertFalse((REPO_ROOT / "lib/schema/core/data/state/assignment.schema.yaml").exists())

    def test_new_ids_are_new_and_removed_ids_remain_reserved(self) -> None:
        registry = yaml.safe_load((REPO_ROOT / "lib/model_ids.yaml").read_text())["model_ids"]
        self.assertEqual(len(registry.values()), len(set(registry.values())))
        self.assertEqual(registry["Mission"], 125)
        self.assertEqual(registry["Reference"], 111)
        self.assertEqual(registry["ArmCommand"], 47)
        self.assertEqual(registry["CombatTask"], 279)
        self.assertEqual(registry["Directive"], 301)
        self.assertEqual(registry["Authority"], 302)
        self.assertEqual(registry["MotionCommand"], 306)
        self.assertEqual(registry["ExecutionCommand"], 308)
        self.assertEqual(registry["CombatTaskProfile"], 309)
        self.assertEqual(OCCID_MODEL_ID_BY_CLASS[Directive], 301)
        self.assertEqual(OCCID_MODEL_ID_BY_CLASS[Authority], 302)
        self.assertEqual(OCCID_MODEL_ID_BY_CLASS[MotionCommand], 306)
        self.assertEqual(occid.OCCID_SCHEMA_VERSION, (5, 0, 0))


if __name__ == "__main__":
    unittest.main()
