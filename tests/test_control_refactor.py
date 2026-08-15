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
    EffectIntent,
    Execution,
    ExecutionCommand,
    GlobalPosition,
    IdentifierType,
    InformationIntent,
    Interface,
    ManeuverIntent,
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
    TaskEffect,
    TaskInformation,
    TaskManeuver,
    TaskTransport,
    TransportIntent,
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


def common_task_values() -> dict:
    return dict(
        record=record_meta("record.task.1"),
        task_id=sid("task.1"),
        instruction="Search Route 6 and establish what vehicle traffic is using it.",
        target_refs=[],
        location_refs=[sid("location.route6")],
        constraints=[],
    )


class ControlRefactorTests(unittest.TestCase):
    def test_control_hierarchy_matches_refactor(self) -> None:
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

    def test_task_has_one_ontology_parent_and_four_practical_schema_children(self) -> None:
        for family in (TaskManeuver, TaskEffect, TaskInformation, TaskTransport):
            self.assertTrue(issubclass(family, Task))

        task_fields = set(Task.model_fields)
        self.assertIn("instruction", task_fields)
        self.assertNotIn("task_type", task_fields)
        self.assertNotIn("task_intent", task_fields)
        self.assertNotIn("intent", task_fields)

        for family in (TaskManeuver, TaskEffect, TaskInformation, TaskTransport):
            self.assertTrue(task_fields.issubset(set(family.model_fields)))
            self.assertIn("intent", family.model_fields)

    def test_task_semantic_roles_are_explicit_runtime_metadata(self) -> None:
        self.assertIsNone(Directive.__dict__["__occid_semantic_role__"])
        self.assertEqual(Task.__dict__["__occid_semantic_role__"], "ontology")
        for family in (TaskManeuver, TaskEffect, TaskInformation, TaskTransport):
            with self.subTest(model=family.__name__):
                self.assertEqual(family.__dict__["__occid_semantic_role__"], "specialization")
        for vocabulary in (ManeuverIntent, EffectIntent, InformationIntent, TransportIntent):
            with self.subTest(enum=vocabulary.__name__):
                self.assertEqual(vocabulary.__dict__["__occid_semantic_role__"], "vocabulary")

    def test_task_intent_vocabularies_are_separate_types(self) -> None:
        self.assertNotEqual(ManeuverIntent, EffectIntent)
        self.assertNotEqual(ManeuverIntent, InformationIntent)
        self.assertNotEqual(ManeuverIntent, TransportIntent)

        values = common_task_values()
        maneuver = TaskManeuver(**values, intent=ManeuverIntent.HOLD)
        effect = TaskEffect(**values, intent=EffectIntent.PROTECT)
        information = TaskInformation(**values, intent=InformationIntent.SEARCH)
        transport = TaskTransport(**values, intent=TransportIntent.EVACUATE)

        for value in (maneuver, effect, information, transport):
            with self.subTest(model=type(value).__name__):
                self.assertEqual(type(value).decode(value.encode()), value)
                self.assertEqual(value.instruction, values["instruction"])
                self.assertEqual(value.location_refs, values["location_refs"])

        with self.assertRaises(ValueError):
            TaskManeuver(**values, intent=InformationIntent.SEARCH)
        with self.assertRaises(ValueError):
            TaskTransport(**values, intent=ManeuverIntent.HOLD)

    def test_task_schema_explicitly_encodes_three_semantic_levels(self) -> None:
        source = yaml.safe_load((REPO_ROOT / "lib/schema/core/control/task.schema.yaml").read_text())
        task = source["models"]["Task"]
        self.assertEqual(task["semantic_role"], "ontology")
        self.assertNotIn("variants", task)
        for name in ("TaskManeuver", "TaskEffect", "TaskInformation", "TaskTransport"):
            self.assertEqual(source["models"][name]["semantic_role"], "specialization")
            self.assertEqual(source["models"][name]["parent"], "Task")
        self.assertEqual(source["models"]["TaskManeuver"]["fields"]["intent"], "ManeuverIntent")
        self.assertEqual(source["models"]["TaskEffect"]["fields"]["intent"], "EffectIntent")
        self.assertEqual(source["models"]["TaskInformation"]["fields"]["intent"], "InformationIntent")
        self.assertEqual(source["models"]["TaskTransport"]["fields"]["intent"], "TransportIntent")
        for name in ("ManeuverIntent", "EffectIntent", "InformationIntent", "TransportIntent"):
            self.assertEqual(source["enums"][name]["semantic_role"], "vocabulary")
            self.assertIn("values", source["enums"][name])
        self.assertNotIn("maps", source)
        self.assertNotIn("TaskType", source["enums"])
        self.assertNotIn("TaskIntent", source["enums"])

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

    def test_removed_classes_are_absent(self) -> None:
        removed = (
            "Mission",
            "IsrTask",
            "MoveTask",
            "HoldTask",
            "ResupplyTask",
            "TaskType",
            "TaskIntent",
            "Task_type",
            "VALID_TASK_INTENT_TYPES",
            "Reference",
            "Mark",
            "ReferencePath",
            "Region",
            "Boundary",
            "FlightCommand",
            "ArmCommand",
            "DisarmCommand",
            "TakeoffCommand",
            "LandCommand",
            "ReturnToLaunchCommand",
            "SetModeCommand",
            "GoToCommand",
            "SetTakeoffAltitudeCommand",
            "SelectMissionCommand",
            "StartOffboardCommand",
            "StopOffboardCommand",
            "TaskCommand",
            "TrackerCommand",
            "ConstraintCondition",
            "ApplyPlanCommand",
            "LowLevelFlightCommand",
            "SetControlAttitudeCommand",
            "SetControlOverrideCommand",
            "NavigationCommand",
            "SetWaypointCommand",
            "ModeCommand",
            "DirectControlCommand",
            "BeginDirectControlCommand",
            "EndDirectControlCommand",
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

    def test_model_id_registry_contains_only_live_models(self) -> None:
        registry = yaml.safe_load((REPO_ROOT / "lib/model_ids.yaml").read_text())["model_ids"]
        live_names = {model.__name__ for model in OCCID_MODEL_ID_BY_CLASS}
        self.assertEqual(set(registry), live_names)
        self.assertEqual(len(registry.values()), len(set(registry.values())))
        self.assertEqual(registry["Directive"], 301)
        self.assertEqual(registry["Authority"], 302)
        self.assertEqual(registry["MotionCommand"], 306)
        self.assertEqual(registry["ExecutionCommand"], 308)
        self.assertEqual(registry["CombatTaskProfile"], 309)
        self.assertEqual(registry["TaskManeuver"], 310)
        self.assertEqual(registry["TaskEffect"], 311)
        self.assertEqual(registry["TaskInformation"], 312)
        self.assertEqual(registry["TaskTransport"], 313)
        self.assertEqual(OCCID_MODEL_ID_BY_CLASS[TaskManeuver], 310)
        self.assertEqual(OCCID_MODEL_ID_BY_CLASS[TaskEffect], 311)
        self.assertEqual(OCCID_MODEL_ID_BY_CLASS[TaskInformation], 312)
        self.assertEqual(OCCID_MODEL_ID_BY_CLASS[TaskTransport], 313)
        self.assertEqual(occid.OCCID_SCHEMA_VERSION, (5, 2, 0))


if __name__ == "__main__":
    unittest.main()
