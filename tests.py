"""Semantic invariants exercised through the live registry and store."""
from occid2 import (
    AmbiguousSemanticMatch, IllegalSemanticCombination, Product, new_store, sem,
    value_semantics,
)


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    store = new_store()
    registry = store.registry
    Drone = registry.product("Drone")
    UAV = registry.product("UAV")
    AirTask = registry.product("AirTask")
    Geodetic = registry.product("Geodetic")
    Airframe = registry.axis("Airframe")
    PhysicalDomain = registry.axis("PhysicalDomain")
    BloodGroup = registry.axis("BloodGroup")
    Representation = registry.axis("Representation")

    # 1. Product multiplication is unordered and idempotent.
    check(sem("Position", "State") == sem("State", "Position", "Position"), "product laws")
    check(isinstance(Drone, Product), "aliases are products")

    # 2. Recursive aliases do not create nominal types.
    check(Drone == UAV * Airframe.MULTIROTOR, "recursive alias expansion")
    check(Geodetic == sem(Representation.Geodetic), "representation alias")
    check(registry.equivalent(Drone, sem(UAV, Airframe.MULTIROTOR)), "normal forms")
    check(registry.entails(Drone, "UnmannedVehicle"), "alias entailment")

    # 3. Axis cardinality is automatic; partial products stay legal.
    check(registry.legal(sem("UnmannedVehicle", PhysicalDomain.AIR)), "partial product")
    check(not registry.legal(sem(PhysicalDomain.LAND, PhysicalDomain.AIR)), "axis cardinality")

    # 4. BloodGroup requires Biological, through declaration ancestry.
    check(registry.entails(sem(BloodGroup.A_POS), "Biological"), "axis requirement")
    check(not registry.legal(sem(Drone, BloodGroup.A_POS)), "derived contradiction")
    check(registry.legal(sem("Person", BloodGroup.A_POS)), "biological applicability")

    # 5. Substrate separates living participants from machines.
    check(not registry.legal(sem("Machine", "Actor")), "substrate contradiction")

    # 6. Charts realize semantic quantities without Python classes.
    coordinates = registry.coordinates(sem("Position", Representation.Geodetic))
    check(set(coordinates) == {"lat", "lon", "h"}, "chart coordinates")
    check({name: coordinate.unit for name, coordinate in coordinates.items()} == {"lat": "deg", "lon": "deg", "h": "m"}, "chart units")
    check(set(registry.coordinates(registry.product("LocalPosition"))) == {"x", "y", "z"}, "local chart")
    check(registry.entails(registry.product("Mark"), "Position"), "Mark denotes position")

    # 7. Different representations answer the same semantic question.
    uav = store.ref("uav-1", "UnmannedVehicle")
    global_position = uav.set(sem("Position", Representation.Geodetic), {"lat": 36.530440, "lon": -83.216383, "h": 125.0})
    local_position = uav.set(sem("Position", Representation.LocalCartesian), {"x": 120.0, "y": -40.0, "z": 15.0})
    check(uav.find("Position") == [global_position, local_position], "broad query")
    check(uav.get("Position", Representation.Geodetic) == global_position, "geodetic narrowing")
    check(uav.get("Position", Representation.LocalCartesian) == local_position, "Cartesian narrowing")
    velocity = uav.set("LocalVelocity", {"vx": 12.0, "vy": 0.0, "vz": -1.5})
    attitude = uav.set("LocalAttitude", {"roll": 0.0, "pitch": 0.0, "yaw": 1.57})
    check(uav.get("Velocity", Representation.LocalCartesian) == velocity, "independent velocity fact")
    check(uav.get("Attitude", Representation.LocalEuler) == attitude, "independent attitude fact")
    check(uav.find("Position") == [global_position, local_position], "quantities remain independent")

    # 8. A representation name is just a product alias; no exact-class shortcut.
    check(uav.get("GlobalPosition") == global_position, "representation alias query")
    try:
        uav.get("Position")
    except AmbiguousSemanticMatch:
        pass
    else:
        raise AssertionError("ambiguity must not pick a representation")

    # 9. A word names an expression; bindings must satisfy typed regions.
    move = store.task("task-move-1", "TaskIntent.MOVE", instruction="move to mark alpha")
    check(move.expression == registry.expression_of("TaskIntent.MOVE"), "word mapping")
    check(move.factors == sem("Task", "Realm.WORLD", "TemporalMode.ACHIEVE"), "fixed factors")
    check(registry.entails(value_semantics(move.ref.get("Task")), move.factors), "task meaning")
    check(move.unbound == ["actor", "destination"], "typed unknowns")
    move.bind("actor", uav)
    try:
        move.bind("destination", uav)
    except TypeError:
        pass
    else:
        raise AssertionError("a vehicle is not a position")
    mark = store.ref("mark-alpha", "Mark")
    mark.set(Geodetic * "Position", {"lat": 36.530440, "lon": -83.216383, "h": 110.0})
    move.bind("destination", mark)
    check(move.unbound == [], "complete binding")

    # 10. A sought unknown is solved when a matching fact arrives.
    target = store.ref("target-42", "UnmannedVehicle")
    locate = store.task("task-locate-1", "TaskIntent.LOCATE")
    locate.bind("target", target)
    check(locate.solve() == {} and target.find("Position") == [], "absent information")
    answer = target.set(Geodetic * "Position", {"lat": 36.530440, "lon": -83.216383, "h": 90.0})
    check(locate.solve()["position"] == answer, "semantic equation")

    # 11. Direction, named roles, and specialization survive without classes.
    assigned = registry.relation_types["AssignedWork"]
    fact = store.relate(assigned, uav, move.ref)
    check(str(fact) == "AssignedWork(assignee=uav-1, work=task-move-1)", "named roles")
    check(fact.operands == (uav, move.ref), "operand order")
    try:
        assigned(move.ref, uav)
    except TypeError:
        pass
    else:
        raise AssertionError("reversed assignment must fail")
    check(fact in store.relations("Directed"), "relation specialization query")

    # 12. Applicability is emergent and does not assert its region.
    check(not registry.entails(sem("Altitude"), PhysicalDomain.AIR), "nonasserting applicability")
    check(registry.legal(sem("Mission", "Altitude")), "partial applicability")
    check(registry.legal(sem("Mission", PhysicalDomain.AIR, "Altitude")), "air applicability")
    check(not registry.legal(sem("Mission", PhysicalDomain.SEA, "Altitude")), "sea contradiction")
    check(registry.applicable(AirTask, "Altitude"), "emergent applicability")

    # 13. Definitions can be introduced while handles and existing data remain live.
    registry.update({"factors": {"ExperimentalPosition": {"implies": ["Position"]}}, "charts": {"ExperimentalPosition": {"native": "bytes"}}})
    experimental = uav.set("ExperimentalPosition", {"native": b"\x01\x02"})
    check(experimental in uav.find("Position"), "runtime entailment")
    check(uav.get("ExperimentalPosition") == experimental, "new representation")

    # 14. Every word resolves; observations do not become commands.
    for word in registry.word_expressions:
        registry.expression_of(word)
    cmd = store.task("command-1", "CommandOperation.MOVE")
    cmd.bind("target", uav).bind("destination", mark)
    check(cmd.expression.name == "DIRECT", "command word")
    check(cmd.unbound == ["path", "radius", "speed", "yaw"], "motion parameters are variables")
    check(cmd.ref.find("Position") == [], "goal is not an observed position")

    # 15. Scalar charts retain units; omitted optionals remain absent.
    window = store.ref("window-1", "TaskTimeWindow")
    value = window.set("TaskTimeWindow", {"earliest_start": 1.0})
    check(value.value == {"earliest_start": 1.0}, "no fabricated latest_finish")
    check(registry.coordinates(sem("TaskTimeWindow"))["earliest_start"].unit == "s", "scalar units")
    check(registry.legal(sem("WeatherLimits", PhysicalDomain.AIR)), "constraint meaning")

    # 16. Useful v1 relations and concepts remain semantic definitions.
    store.relate("ConstrainedBy", subject=cmd.ref, constraint=window)
    authority = store.ref("authority-1", "Authority")
    store.relate("Holds", authority=authority, holder=uav)
    try:
        store.relate("ConstrainedBy", uav, window)
    except TypeError:
        pass
    else:
        raise AssertionError("a vehicle is not directed work")
    check(registry.entails(sem("Task"), "Directive"), "Task ancestry")
    check(registry.entails(sem("Command"), "Directive"), "Command ancestry")
    check(registry.entails(sem("Predicate"), "Condition"), "condition ancestry")

    # 17. Unknown, absent, and illegal information remain separate.
    opaque = uav.set("Irreducible.FutureConcept", {"unrecognized": 42})
    check(uav.get("Irreducible.FutureConcept") == opaque, "opaque information")
    check(uav.find("Unseen.FutureConcept") == [], "unknown query")
    try:
        uav.find("Mission", PhysicalDomain.SEA, "Altitude")
    except IllegalSemanticCombination:
        pass
    else:
        raise AssertionError("illegal query must be distinguished from absence")
    print("17 semantic invariant groups passed")


if __name__ == "__main__":
    main()
