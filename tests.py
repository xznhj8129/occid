from __future__ import annotations

import hashlib
import tempfile
from dataclasses import fields
from pathlib import Path

from compiler import compile_schema
from runtime import Product, sem, value_semantics
from generated.occid2 import (
    AirMission,
    AirTask,
    Airframe,
    Actor,
    Altitude,
    Biological,
    BloodGroup,
    Destination,
    PhysicalDomain,
    Drone,
    EffectIntent,
    Existence,
    Frame,
    GlobalPosition,
    InformationIntent,
    Machine,
    ManeuverIntent,
    Mark,
    Mission,
    Person,
    Position,
    Realm,
    Target,
    Task,
    TaskEffect,
    TaskInformation,
    TaskManeuver,
    TemporalMode,
    TruthTarget,
    UAV,
    UnmannedVehicle,
    new_store,
)

ROOT = Path(__file__).parent


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    store = new_store()
    registry = store.registry

    # 1. Normal parentage provides inherited fields.
    task_fields = {f.name for f in fields(TaskManeuver)}
    check({"uid", "instruction", "priority", "status", "intent"} <= task_fields, "Task field inheritance failed")

    # 2. Aliases are products, not classes. Recursive expansion is canonical.
    check(isinstance(Drone, Product), "Drone must be a product, not a class")
    check(registry.entails(Drone, UnmannedVehicle), "Drone must entail UnmannedVehicle")
    check(registry.entails(Drone, PhysicalDomain.AIR), "Drone must entail PhysicalDomain.AIR")
    check(registry.entails(Drone, Airframe.MULTIROTOR), "Drone must entail its airframe")
    check(Drone == sem(UAV, Airframe.MULTIROTOR), "Drone must equal UAV × Airframe.MULTIROTOR")
    check(AirMission == sem(Mission, PhysicalDomain.AIR), "AirMission must equal Mission × PhysicalDomain.AIR")

    # 3. Axis cardinality is automatic; partial products stay legal.
    check(registry.legal(sem(UnmannedVehicle, PhysicalDomain.AIR)), "single-domain partial product is legal")
    check(not registry.legal(sem(UnmannedVehicle, PhysicalDomain.LAND, PhysicalDomain.AIR)), "two domains contradict")

    # 4. The BloodGroup contradiction is derived, not declared.
    check(registry.entails(sem(BloodGroup.A_POS), Biological), "BloodGroup must entail Biological")
    check(not registry.legal(sem(Drone, BloodGroup.A_POS)), "Drone cannot have a blood group")
    check(registry.legal(sem(Person, BloodGroup.A_POS)), "Person accepts a blood group")

    # 5. Biological fixed: substrate cardinality separates living from machine.
    check(not registry.legal(sem(Machine, Actor)), "Machine × Actor clashes on Substrate")

    # 6. Exact class lookup and semantic lookup return the same stored value.
    uav = store.ref("uav-1", UnmannedVehicle)
    gp = GlobalPosition(lat=45.30, lon=-74.20, alt_m=125.0)
    uav.set(gp)
    check(uav.get(GlobalPosition) is gp, "exact representation lookup failed")
    check(uav.get(Position, Frame.WGS84) is gp, "semantic position lookup failed")

    # 7. A Mark is semantically a point, so it answers the Position question.
    mark = Mark(uid="mark-alpha", name="alpha")
    mark_ref = store.ref("mark-alpha", Mark)
    mark_ref.set(mark)
    check(mark_ref.get(GlobalPosition) is mark, "Mark must answer the GlobalPosition question")
    many = store.get_many([uav, mark_ref], Position)
    check(many == {"uav-1": gp, "mark-alpha": mark}, "get_many failed")

    # 8. Surface vocabulary entails its factored product.
    move = TaskManeuver(uid="task-move", instruction="move", intent=ManeuverIntent.MOVE)
    check(
        registry.entails(value_semantics(move), sem(Task, Realm.WORLD, TemporalMode.ACHIEVE, Position)),
        "MOVE factorization failed",
    )
    locate = TaskInformation(uid="task-locate", instruction="locate", intent=InformationIntent.LOCATE)
    check(
        registry.entails(value_semantics(locate), sem(Task, Realm.INFORMATION, TemporalMode.ACHIEVE, Position)),
        "LOCATE factorization failed",
    )
    create = TaskEffect(uid="task-create", instruction="create", intent=EffectIntent.CREATE)
    check(
        registry.entails(
            value_semantics(create),
            sem(Task, Realm.WORLD, TemporalMode.ACHIEVE, Existence, TruthTarget.TRUE),
        ),
        "CREATE factorization failed",
    )

    # 9. Relations are directed and operands are validated semantically.
    task_ref = store.ref("task-move", TaskManeuver)
    task_ref.set(move)
    fact = store.relate(Destination, task_ref, mark_ref)
    check(str(fact) == "Destination(task-move, mark-alpha)", "Destination relation failed")
    check(fact.operands == (task_ref, mark_ref), "relation operand order lost")
    try:
        Destination(mark_ref, task_ref)
    except TypeError:
        pass
    else:
        raise AssertionError("Mark is not a task; reversed Destination must fail")
    store.relate(Target, task_ref, uav)
    check(len(store.relations(Target)) == 1, "Target relation missing")

    # 10. Codewords declare the relations they open without flattening them.
    check(registry.codeword_relation(ManeuverIntent.MOVE) == "Destination", "MOVE must open Destination")
    check(registry.codeword_relation(InformationIntent.LOCATE) == "Target", "LOCATE must open Target")

    # 11. Applicability is emergent and never asserts.
    check(not registry.entails(sem(Altitude), PhysicalDomain.AIR), "applicability must not assert")
    check(registry.legal(sem(Mission, Altitude)), "Mission × Altitude is unknown, not illegal")
    check(registry.legal(sem(Mission, PhysicalDomain.AIR, Altitude)), "Altitude is meaningful in air")
    check(not registry.legal(sem(Mission, PhysicalDomain.SEA, Altitude)), "Altitude is meaningless at sea")
    check(registry.applicable(sem(Mission, PhysicalDomain.AIR), Altitude), "Mission × AIR gains Altitude")
    check(not registry.applicable(sem(Mission, PhysicalDomain.SEA), Altitude), "Mission × SEA lacks Altitude")
    check(registry.applicable(AirTask, Altitude), "AirTask = Task × AIR gains Altitude")

    # 12. Unknown answer and illegal question are distinct.
    empty = store.ref("empty-1", UnmannedVehicle)
    check(empty.find(Position) == [], "no datum is unknown, not illegal")
    check(not registry.legal(sem(UnmannedVehicle, BloodGroup.A_POS)), "blood group for a vehicle is illegal")

    # 13. Compiler output is deterministic.
    with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
        compile_schema(ROOT / "occid2.schema.yaml", Path(a))
        compile_schema(ROOT / "occid2.schema.yaml", Path(b))
        for filename in ("occid2.py", "semantic_registry.json"):
            ha = hashlib.sha256((Path(a) / filename).read_bytes()).digest()
            hb = hashlib.sha256((Path(b) / filename).read_bytes()).digest()
            check(ha == hb, f"nondeterministic compiler output: {filename}")

    print("13 tests passed")


if __name__ == "__main__":
    main()
