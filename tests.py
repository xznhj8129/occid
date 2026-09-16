from __future__ import annotations

import hashlib
import shutil
import tempfile
from dataclasses import fields
from pathlib import Path

from compiler import compile_schema
from runtime import sem, value_semantics
from generated.occid2 import (
    BloodGroup,
    Destination,
    Domain,
    Drone,
    EffectIntent,
    Existence,
    Frame,
    GlobalPosition,
    GroundRobot,
    InformationIntent,
    ManeuverIntent,
    Mark,
    Person,
    Position,
    Realm,
    Task,
    TaskEffect,
    TaskInformation,
    TaskManeuver,
    TemporalMode,
    TruthTarget,
    new_store,
)

ROOT = Path(__file__).parent


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    store = new_store()

    # 1. One normal parent tree provides inherited fields.
    task_fields = {f.name for f in fields(TaskManeuver)}
    check({"uid", "instruction", "priority", "status", "intent"} <= task_fields, "Task field inheritance failed")

    # 2. The old spatial assumptions are not on Task.
    check("location_uids" not in task_fields and "target_uids" not in task_fields, "Task still contains non-universal spatial fields")

    # 3. Drone semantics are factored, not encoded as semantic fields.
    check(store.registry.entails(Drone._semantics, Domain.AIR), "Drone must entail AIR")
    check("domain" not in {f.name for f in fields(Drone)}, "Domain leaked back into representation fields")

    # 4. Axis cardinality catches an indirect contradiction.
    check(not store.registry.legal(sem(Drone, Domain.LAND)), "Drone × LAND must be illegal")

    # 5. Applicability + Substrate cardinality derives BloodGroup contradiction.
    check(not store.registry.legal(sem(Drone, BloodGroup.A_POS)), "Mechanical drone cannot have a blood group")
    check(store.registry.legal(sem(Person, BloodGroup.A_POS)), "Biological person should accept blood group")

    # 6. Exact representation lookup and semantic lookup return the same stored value.
    drone = store.ref("drone-1", Drone)
    gp = GlobalPosition(lat=45.3, lon=-74.2, alt_m=125.0)
    drone.set(gp)
    check(drone.get(GlobalPosition) is gp, "exact representation lookup failed")
    check(drone.get(Position, Frame.WGS84) is gp, "semantic position lookup failed")

    # 7. Multiple subjects remain explicit in the API.
    rover = store.ref("rover-1", GroundRobot)
    rp = GlobalPosition(lat=45.31, lon=-74.22, alt_m=2.0)
    rover.set(rp)
    many = store.get_many([drone, rover], Position)
    check(many == {"drone-1": gp, "rover-1": rp}, "get_many failed")

    # 8. MOVE is a surface codeword over reusable semantic factors.
    move = TaskManeuver(uid="task-move", instruction="move", intent=ManeuverIntent.MOVE)
    expected_move = sem(Task, Realm.WORLD, TemporalMode.ACHIEVE, Position)
    check(store.registry.equivalent(value_semantics(move), expected_move), "MOVE factorization failed")

    # 9. LOCATE differs from MOVE only in the appropriate semantic coordinates.
    locate = TaskInformation(uid="task-locate", instruction="locate", intent=InformationIntent.LOCATE)
    expected_locate = sem(Task, Realm.INFORMATION, TemporalMode.ACHIEVE, Position)
    check(store.registry.equivalent(value_semantics(locate), expected_locate), "LOCATE factorization failed")

    # 10. CREATE uses state-specific TruthTarget rather than a giant Action axis.
    create = TaskEffect(uid="task-create", instruction="create", intent=EffectIntent.CREATE)
    expected_create = sem(Task, Realm.WORLD, TemporalMode.ACHIEVE, Existence, TruthTarget.TRUE)
    check(store.registry.equivalent(value_semantics(create), expected_create), "CREATE factorization failed")

    # 11. Relations bind multiple semantic things and preserve operand roles.
    task_ref = store.ref("task-move", TaskManeuver)
    mark_ref = store.ref("mark-a", Mark)
    fact = store.relate(Destination, task_ref, mark_ref)
    check(str(fact) == "Destination(task-move, mark-a)", "Destination relation failed")
    try:
        Destination(mark_ref, task_ref)
    except TypeError:
        pass
    else:
        raise AssertionError("reversed Destination relation should fail")

    # 12. Semantic discovery can use meaning supplied by an enum field.
    task_ref.set(move)
    matches = task_ref.find(Position)
    check(matches == [move], "semantic discovery over task intent failed")

    # 13. Representation class remains the source of its static meaning.
    check(store.registry.entails(GlobalPosition._semantics, Position), "GlobalPosition semantics missing Position")
    check(store.registry.entails(GlobalPosition._semantics, Frame.WGS84), "GlobalPosition semantics missing WGS84")

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
