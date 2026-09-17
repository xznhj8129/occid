from __future__ import annotations

import hashlib
import tempfile
from dataclasses import fields
from pathlib import Path

from compiler import compile_schema
from runtime import Product, sem, value_semantics
from generated.occid2 import (
    AirTask,
    Airframe,
    Altitude,
    Actor,
    AssignedWork,
    Biological,
    BloodGroup,
    Directed,
    Drone,
    Geodetic,
    GlobalPosition,
    InformationIntent,
    LocalAttitude,
    LocalPosition,
    LocalVelocity,
    Machine,
    ManeuverIntent,
    Mark,
    Mission,
    MOVE,
    Person,
    PhysicalDomain,
    Position,
    Realm,
    Representation,
    Task,
    TaskInformation,
    TaskManeuver,
    TemporalMode,
    UAV,
    UnmannedVehicle,
    VehicleState,
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
    task_fields = {field.name for field in fields(TaskManeuver)}
    check({"uid", "instruction", "priority", "status", "intent"} <= task_fields, "Task field inheritance failed")

    # 2. Aliases are products, not classes. Recursive expansion is canonical.
    check(isinstance(Drone, Product), "Drone must be a product, not a class")
    check(registry.entails(Drone, UnmannedVehicle), "Drone must entail UnmannedVehicle")
    check(registry.entails(Drone, PhysicalDomain.AIR), "Drone must entail PhysicalDomain.AIR")
    check(registry.entails(Drone, Airframe.MULTIROTOR), "Drone must entail its airframe")
    check(Drone == sem(UAV, Airframe.MULTIROTOR), "Drone must equal UAV * Airframe.MULTIROTOR")
    check(Geodetic == sem(Representation.Geodetic), "Geodetic must equal Representation.Geodetic")
    check(registry.equivalent(Drone, sem(UAV, Airframe.MULTIROTOR)), "named and unnamed products must be equivalent")

    # 3. Axis cardinality is automatic; partial products stay legal.
    check(registry.legal(sem(UnmannedVehicle, PhysicalDomain.AIR)), "single-domain partial product is legal")
    check(not registry.legal(sem(UnmannedVehicle, PhysicalDomain.LAND, PhysicalDomain.AIR)), "two domains contradict")

    # 4. The BloodGroup contradiction is derived, not declared.
    check(registry.entails(sem(BloodGroup.A_POS), Biological), "BloodGroup must entail Biological")
    check(not registry.legal(sem(Drone, BloodGroup.A_POS)), "Drone cannot have a blood group")
    check(registry.legal(sem(Person, BloodGroup.A_POS)), "Person accepts a blood group")

    # 5. Substrate cardinality separates living from machine.
    check(not registry.legal(sem(Machine, Actor)), "Machine * Actor clashes on Substrate")

    # 6. Charts produce irreducible variables; units stay metadata.
    check({field.name for field in fields(GlobalPosition)} == {"lat", "lon", "h"}, "geodetic chart fields")
    check(GlobalPosition._units == {"lat": "deg", "lon": "deg", "h": "m"}, "geodetic chart units")
    check({field.name for field in fields(LocalPosition)} == {"x", "y", "z"}, "local cartesian chart fields")
    check({field.name for field in fields(Mark)} == {"uid", "name", "lat", "lon", "h"}, "Mark compiles its chart")

    # 7. A projection is the compiled normal form of chart-selected facts.
    check(
        {field.name for field in fields(VehicleState)}
        == {"uid", "lat", "lon", "h", "vx", "vy", "vz", "roll", "pitch", "yaw"},
        "VehicleState normal form",
    )
    uav = store.ref("uav-1", UnmannedVehicle)
    uav.set(GlobalPosition(lat=45.30, lon=-74.20, h=125.0))
    partial = store.project(uav, VehicleState)
    check(partial.lat == 45.30 and partial.vy is None, "a partial projection leaves unknown coordinates unset")
    uav.set(LocalVelocity(vx=12.0, vy=0.0, vz=-1.5))
    uav.set(LocalAttitude(roll=0.0, pitch=0.0, yaw=1.57))
    full = store.project(uav, VehicleState)
    check(full.uid == "uav-1" and (full.lat, full.vy, full.yaw) == (45.30, 0.0, 1.57), "projection materialization failed")

    # 8. The representation is selected by factors, not by class paths.
    uav.set(LocalPosition(x=120.0, y=-40.0, z=15.0))
    check(len(uav.find(Position)) == 2, "both representations answer the Position question")
    check(uav.get(Position, Representation.Geodetic).lon == -74.20, "geodetic narrowing failed")
    check(uav.get(Position, Representation.LocalCartesian).x == 120.0, "local narrowing failed")

    # 9. Exact class lookup and semantic lookup return the same stored value.
    check(uav.get(GlobalPosition).lat == 45.30, "exact representation lookup failed")

    # 10. A word names an expression; the task realizes it.
    move = store.task(
        "task-move-1", TaskManeuver, ManeuverIntent.MOVE, instruction="move to mark alpha"
    )
    check(registry.expression_of(ManeuverIntent.MOVE) == MOVE, "MOVE word must name MOVE expression")
    check(
        MOVE.factors == sem(Task, Realm.WORLD, TemporalMode.ACHIEVE),
        "MOVE factors must be the declared product",
    )
    check(move.expression.name == "MOVE", "task must realize MOVE")
    check(move.ref.get(TaskManeuver).intent is ManeuverIntent.MOVE, "the word stores the vocabulary member")
    check(
        registry.entails(value_semantics(move.ref.get(TaskManeuver)), MOVE.factors),
        "task value must entail the expression factors",
    )
    check(move.unbound == ["actor", "destination"], "unbound variables")
    move.bind("actor", uav)
    try:
        move.bind("destination", uav)
    except TypeError:
        pass
    else:
        raise AssertionError("a vehicle does not satisfy the Position region")
    mark_ref = store.ref("mark-alpha", Mark)
    mark_ref.set(Mark(uid="mark-alpha", name="alpha", lat=45.28, lon=-74.18, h=110.0))
    move.bind("destination", mark_ref)
    check(move.unbound == [], "all variables bound")

    # 11. An unbound variable is an unknown, not an error.
    target = store.ref("target-42", UnmannedVehicle)
    locate = store.task(
        "task-locate-1", TaskInformation, InformationIntent.LOCATE, instruction="locate target-42"
    )
    locate.bind("target", target)
    check(locate.solve() == {}, "an entity without a position has an unknown answer")
    check(target.find(Position) == [], "no datum is unknown, not illegal")
    target.set(GlobalPosition(lat=45.10, lon=-74.40, h=90.0))
    solved = locate.solve()
    check(solved["position"].lat == 45.10, "the answer appears once the fact exists")

    # 12. Relations are directed, roles are named, and operands are validated.
    fact = store.relate(AssignedWork, uav, move.ref)
    check(str(fact) == "AssignedWork(assignee=uav-1, work=task-move-1)", "named roles failed")
    check(fact.operands == (uav, move.ref), "relation operand order lost")
    try:
        AssignedWork(move.ref, uav)
    except TypeError:
        pass
    else:
        raise AssertionError("reversed AssignedWork must fail")
    check(AssignedWork.specializes(Directed), "relation specialization failed")
    check(fact in store.relations(Directed), "base relation query must see specializations")

    # 13. Applicability is emergent and never asserts.
    check(not registry.entails(sem(Altitude), PhysicalDomain.AIR), "applicability must not assert")
    check(registry.legal(sem(Mission, Altitude)), "Mission * Altitude is unknown, not illegal")
    check(registry.legal(sem(Mission, PhysicalDomain.AIR, Altitude)), "Altitude is meaningful in air")
    check(not registry.legal(sem(Mission, PhysicalDomain.SEA, Altitude)), "Altitude is meaningless at sea")
    check(registry.applicable(AirTask, Altitude), "AirTask = Task * AIR gains Altitude")

    # 14. Compiler output is deterministic.
    with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
        compile_schema(ROOT / "occid2.schema.yaml", Path(a))
        compile_schema(ROOT / "occid2.schema.yaml", Path(b))
        for filename in ("occid2.py", "semantic_registry.json"):
            ha = hashlib.sha256((Path(a) / filename).read_bytes()).digest()
            hb = hashlib.sha256((Path(b) / filename).read_bytes()).digest()
            check(ha == hb, f"nondeterministic compiler output: {filename}")

    print("14 tests passed")


if __name__ == "__main__":
    main()
