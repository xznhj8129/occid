"""Executable semantic algebra, live extension, and wire exchange demo."""

from occid2 import (
    AmbiguousSemanticMatch, IllegalSemanticCombination, Query, SemanticValue, decode, new_store, sem,
)


PREDICATE = SemanticValue(sem("Predicate"), {
    "subject_uid": "uav-1", "quantity": "Height", "value": 125.0,
})
LOGIC = SemanticValue(sem("BooleanLogic"), {
    "operator": "AND", "terms": [PREDICATE, PREDICATE],
})
WEATHER = {
    "condition": LOGIC, "ifr": True, "night": False, "icing": False,
    "rain": {"min_value": 0.0, "max_value": 2.0},
    "snow": {"max_value": 0.0}, "temp": {"min_value": -5.0, "max_value": 35.0},
    "wind": {"min_value": 0.0, "max_value": 12.0}, "vis": {"min_value": 3.0},
    "unresolved_source_extension": b"\x00\xff",
}
OBJECTIVE = {
    "uid": "objective-1", "name": "reach the destination", "condition": LOGIC,
    "criteria": [PREDICATE, LOGIC, PREDICATE], "priority": 1, "status": "ACTIVE",
    "start_time": 1.0, "deadline": 120.0,
}
PATH = {"points": [
    {"lat": 36.530440, "lon": -83.216383, "h": 125.0},
    {"lat": 36.530440, "lon": -83.216383, "h": 130.0},
    {"lat": 36.530440, "lon": -83.216383, "h": 125.0},
]}


def compositions(store) -> None:
    registry = store.registry
    weather_ref = store.ref("weather-1", "WeatherLimits")
    weather = weather_ref.set("WeatherLimits", WEATHER, source="operator", observed_at=1)
    objective_ref = store.ref("objective-1", "Objective")
    objective = objective_ref.set("Objective", OBJECTIVE, source="operator")
    path_ref = store.ref("path-1", "GeoPath")
    path = path_ref.set("GeoPath", PATH, source="operator")
    move = store.task("composed-task", "TaskIntent.MOVE", instruction="follow the approved route", priority="IMMEDIATE", status="NEW")
    move.bind("actor", store.ref("uav-1")).bind("destination", store.ref("mark-alpha"))
    store.relate("ConstrainedBy", subject=move.ref, constraint=weather_ref)
    store.relate("OwnedBy", objective=objective_ref, owner=store.ref("uav-1"))

    # Query a role-bearing quantity, not 'wind.max_value' or a containing type.
    upper_wind = weather_ref.get("WeatherQuantity.Wind", "Bound.Upper")
    assert upper_wind.value == 12.0 and upper_wind.source == "operator"
    assert weather_ref.get("PermissionKind.Night").value is False
    assert len(objective.find("Predicate", "ConditionRole.Criterion")) == 4
    assert objective.get("Priority", "Urgency.HIGH").value == 1
    assert objective.get("Time", "TimeRole.Deadline").unit == "s"
    assert objective.find("ConditionRole.Requirement", "Reference")[0].referent(store).uid == "uav-1"
    waypoints = path_ref.find("Position", "PathRole.Waypoint")
    assert [part.ordinal for part in waypoints] == [0, 1, 2]
    assert waypoints[0].value == waypoints[2].value and waypoints[0].id != waypoints[2].id
    assert [part.value for part in path_ref.find("Height", "PathRole.Waypoint")] == [125.0, 130.0, 125.0]
    assert move.ref.get("Text", "TextRole.Instruction").value == "follow the approved route"
    assert move.ref.get("Intent").expression.name == "MOVE"
    assert move.get("Participation.Actor").referent(store).uid == "uav-1"

    for datum in (weather, objective, path, move.ref.get("Task")):
        tree = datum.decompose()
        assert tree.recompose(tree.leaves()) == datum.value
        assert decode(datum.encode()) == datum
        assert tree.links()[0].roles["whole"] == tree

    # Compose from semantic values. No authored source field is needed here.
    range_value = registry.compose("NumericRange",
        SemanticValue(sem("Scalar", "Bound.Lower"), 0.0),
        SemanticValue(sem("Scalar", "Bound.Upper"), 12.0))
    limits = registry.compose("WeatherLimits",
        SemanticValue(range_value.semantics * "WeatherQuantity.Wind", range_value.value),
        SemanticValue(sem("Permission", "PermissionKind.Night"), False))
    rebuilt = store.ref("rebuilt-limits").set("WeatherLimits", limits)
    assert rebuilt.get("WeatherQuantity.Wind", "Bound.Upper").value == 12.0
    rebuilt_path = registry.compose("GeoPath", *waypoints)
    assert rebuilt_path.value["points"][0].value == PATH["points"][0]
    assert len(rebuilt_path.value["points"]) == 3

    # The same latitude can arrive under a completely different coordinate name.
    registry.update({
        "factors": {"SurveyFix": {"implies": ["State"]}},
        "charts": {"SurveyFix": {"north_angle": {"semantics": "Latitude", "type": "float", "unit": "deg"}}},
    })
    survey = store.ref("survey-1").set("SurveyFix", {"north_angle": 36.530440})
    assert survey.get("Latitude").value == path.find("Latitude")[0].value
    recomposed_survey = registry.compose("SurveyFix", path.find("Latitude")[0])
    assert registry.decompose("SurveyFix", recomposed_survey).get("Latitude").value == 36.530440
    print("\nStructured meaning: tasks, predicates, weather limits, objectives, and paths.")
    print("  Wind x UpperBound ->", upper_wind.value, "; no field path")
    print("  Criterion predicates retain their nested roles and repeated occurrences.")
    print("  Ordered path heights ->", [part.value for part in path_ref.find("Height")])
    print("  Chart inversion reconstructs every supplied value, including unknown extensions.")
    print("  Semantic composition selects variables; a new chart changes coordinate spelling only.")


def run() -> None:
    store = new_store()
    registry = store.registry
    Position = registry.product("Position")
    Representation = registry.axis("Representation")
    AltitudeReference = registry.axis("AltitudeReference")
    Drone = registry.product("Drone")
    UAV = registry.product("UAV")
    Airframe = registry.axis("Airframe")
    assert Drone == UAV * Airframe.MULTIROTOR
    assert registry.entails(Drone, sem("Machine", "Controller.UNMANNED", "PhysicalDomain.AIR"))
    assert not registry.legal(sem(Drone, "BloodGroup.A_POS"))
    assert not registry.legal(sem("Machine", "Actor"))
    assert registry.legal(sem("Mission", "Altitude"))
    assert registry.legal(sem("Mission", "PhysicalDomain.AIR", "Altitude"))
    assert not registry.legal(sem("Mission", "PhysicalDomain.SEA", "Altitude"))
    print("Aliases are products; cardinality, legality, and entailment follow declarations.")
    print("  Drone =", Drone)
    for chart in registry.charts[:5]:
        print(" ", chart)

    uav = store.ref("uav-1", UAV)
    position = uav.set(
        Position * Representation.Geodetic * AltitudeReference.WGS84Ellipsoid,
        {"lat": 36.530440, "lon": -83.216383, "h": 125.0},
        source={"protocol": "MAVLink", "representation": "chart-unit position observation"},
        observed_at="2026-10-10T12:00:00Z",
        provenance={"kind": "observation"},
    )
    assert uav.find(Position) == [position]
    assert uav.get(Position, Representation.Geodetic).value["lon"] == -83.216383
    print("\nStore a geodetic position with no representation class.")
    print("  uav.find(Position) ->", [datum.value for datum in uav.find(Position)])
    print("  uav.get(Position, Representation.Geodetic) ->", position.value)
    assert decode(position.encode()) == position

    local = uav.set(
        Position * Representation.LocalCartesian,
        {"x": 120.0, "y": -40.0, "z": 15.0},
        source="local sensor", observed_at="2026-10-10T12:00:01Z",
        provenance={"kind": "observation", "frame": "site-1 ENU", "origin": position.id},
    )
    assert uav.find(Position) == [position, local]
    assert uav.get(Position, Representation.LocalCartesian) == local
    print("  A second representation coexists ->", len(uav.find(Position)), "position facts")
    try:
        uav.get(Position)
    except AmbiguousSemanticMatch:
        print("  uav.get(Position) -> ambiguous")
    else:
        raise AssertionError("broad position lookup must expose ambiguity")
    empty = store.ref("empty", "Entity")
    assert empty.find(Position) == []
    try:
        empty.get(Position)
    except KeyError:
        print("  empty.get(Position) -> absent")
    else:
        raise AssertionError("absent position must remain unknown")
    try:
        empty.find("Mission", "PhysicalDomain.SEA", "Altitude")
    except IllegalSemanticCombination:
        print("  Mission x SEA x Altitude -> illegal")
    else:
        raise AssertionError("illegal combination must not return an empty result")

    velocity = uav.set(sem("Velocity", Representation.LocalCartesian), {"vx": 12.0, "vy": 0.0, "vz": -1.5}, source="velocity sensor")
    attitude = uav.set(sem("Attitude", Representation.LocalEuler), {"roll": 0.0, "pitch": 0.0, "yaw": 1.57}, source="attitude sensor")
    assert uav.get("Velocity", Representation.LocalCartesian) == velocity
    assert uav.get("Attitude", Representation.LocalEuler) == attitude
    assert uav.find(Position) == [position, local]
    print("  Independent velocity and attitude facts ->", velocity.value, attitude.value)

    # This handle remains usable when its axis gains a value during execution.
    registry.update({
        "axes": {"Representation": {**registry.spec["axes"]["Representation"], "values": [*registry.spec["axes"]["Representation"]["values"], "Polar"]}},
        "charts": {"Position * Representation.Polar": {"coords": {"range": "float[m]", "bearing": "float[rad]", "elevation": "float[rad]"}, "context": {"frame": "radar-1"}}},
    })
    polar = uav.set(Position * Representation.Polar, {"range": 130.0, "bearing": 0.4, "elevation": 0.1}, source="radar", observed_at="2026-10-10T12:00:02Z", provenance={"frame": "radar-1"})
    assert polar in uav.find(Position)
    print("\nLive chart extension ->", len(uav.find(Position)), "position representations; no regeneration")
    opaque = uav.set("SensorReading", {"native": b"\x01\x02", "unknown": None}, source="future sensor")
    assert uav.get("SensorReading") == opaque
    recorded = opaque.encode()
    registry.update({"factors": {"SensorReading": {"implies": ["Position"]}}})
    assert opaque in uav.find(Position)
    assert opaque not in uav.find(Query(Position, interpretation="recorded"))
    assert "Position" not in opaque.meaning
    assert "Position" in store.meaning_of(opaque)
    assert opaque.encode() == recorded
    print("  Learned entailment finds earlier evidence; recorded meaning and source value stay unchanged.")

    move = store.task("task-move-1", "TaskIntent.MOVE", instruction="move to mark alpha")
    assert move.unbound == ["actor", "destination"]
    move.bind("actor", uav)
    mark = store.ref("mark-alpha", "Mark")
    mark.set(Position * Representation.Geodetic, {"lat": 36.530440, "lon": -83.216383, "h": 110.0}, source="operator")
    move.bind("destination", mark)
    assert move.unbound == []
    target = store.ref("target-42", "UnmannedVehicle")
    locate = store.task("task-locate-1", "TaskIntent.LOCATE", instruction="locate target-42")
    locate.bind("target", target)
    assert locate.solve() == {}
    answer = target.set(Position * Representation.Geodetic, {"lat": 36.530440, "lon": -83.216383, "h": 90.0}, source="target sensor", observed_at="2026-10-10T12:00:00Z", validity={"from": "2026-10-10T12:00:00Z", "to": "2026-10-10T12:01:00Z"}, provenance={"kind": "observation"})
    assert locate.solve()["position"] == answer
    print("\nOpen expressions keep typed unknowns and solve when facts arrive.")
    print(" ", move)
    print(" ", locate, "->", locate.solve()["position"].value)
    next_answer = target.set(Position * Representation.Geodetic, {"lat": 36.530440, "lon": -83.216383, "h": 91.0}, source="target sensor", observed_at="2026-10-10T12:00:01Z", validity={"from": "2026-10-10T12:00:01Z", "to": "2026-10-10T12:01:00Z"}, provenance={"kind": "observation"})
    try:
        locate.solve()
    except AmbiguousSemanticMatch:
        print("  Repeated observations leave unconstrained LOCATE ambiguous.")
    else:
        raise AssertionError("LOCATE must not silently select a later observation")
    question = Query(source="target sensor", latest=True, observed_before="2026-10-10T12:00:02Z", valid_at="2026-10-10T12:00:02Z", provenance={"kind": "observation"})
    assert locate.solve(position=question)["position"] == next_answer
    print("  Explicit source, validity, and latest constraints ->", next_answer.value)
    assignment = store.relate("AssignedWork", assignee=uav, work=move.ref)
    assert assignment.roles["assignee"].uid == "uav-1"
    assert assignment in store.relations("Directed")
    try:
        store.relate("AssignedWork", assignee=move.ref, work=uav)
    except TypeError:
        print("  Directed roles validated:", assignment)
    else:
        raise AssertionError("reversed assignment must be rejected")

    another = uav.set(Position * Representation.Geodetic * AltitudeReference.WGS84Ellipsoid, {"lat": 36.530440, "lon": -83.216383, "h": 126.0}, source="second sensor", observed_at="2026-10-10T12:00:03Z")
    assert another.id != position.id
    assert len(uav.find(Position, Representation.Geodetic)) == 2
    print("\nSeveral sources and observation times remain independent facts.")
    revision = registry.definition_id
    try:
        registry.update({"aliases": {"Broken": ["MissingDefinition"]}})
    except ValueError:
        assert registry.definition_id == revision
        assert registry.legal(Drone)
        print("  Invalid definition rejected; current registry unchanged")
    else:
        raise AssertionError("invalid registry update accepted")

    registry.update({"mappings": {"position-report": {"semantics": ["Position", "Representation.Geodetic", "AltitudeReference.WGS84Ellipsoid"], "fields": {"lat": "latitude", "lon": "longitude", "h": "ellipsoid_height"}, "context": {"units": {"latitude": "deg", "longitude": "deg", "ellipsoid_height": "m"}}}}})
    report = store.ref("report-subject", "Entity")
    raw = report.set(sem(), {"latitude": 36.530440, "longitude": -83.216383, "ellipsoid_height": 125.0, "msl_height": 110.0, "unknown_source_field": b"\xff\x00"}, source="external position report", observed_at=1234)
    mapped = store.interpret(raw, "position-report")
    registry.update({"mappings": {"position-report": {"semantics": ["Position", "Representation.Geodetic", "AltitudeReference.MeanSeaLevel"], "fields": {"lat": "latitude", "lon": "longitude", "h": "msl_height"}, "context": {"units": {"latitude": "deg", "longitude": "deg", "msl_height": "m"}}}}})
    revised = store.interpret(raw, "position-report")
    assert mapped.value["h"] == 125.0 and revised.value["h"] == 110.0
    assert mapped.definition_id != revised.definition_id
    assert mapped.provenance["derived_from"] == revised.provenance["derived_from"] == [raw.id]
    assert report.get(Position, AltitudeReference.WGS84Ellipsoid) == mapped
    assert report.get(Position, AltitudeReference.MeanSeaLevel) == revised
    assert not registry.legal(Position * AltitudeReference.WGS84Ellipsoid * AltitudeReference.MeanSeaLevel)
    print("\nMapping revision creates a new interpretation and retains the complete source report.")
    print("  Semantic altitude references distinguish ellipsoid height 125 m from MSL height 110 m.")
    assert store.expression("task-move-1").unbound == []
    assert store.expression("task-locate-1").solve(position=question)["position"] == next_answer
    assert store.relations("AssignedWork")[0].roles["work"].uid == "task-move-1"
    assert report.find()[0].value == raw.value
    assert [datum.value["h"] for datum in report.find("Position")] == [125.0, 110.0]
    assert decode(raw.encode()) == raw
    assert decode(mapped.encode()) == mapped
    assert decode(revised.encode()) == revised
    compact = revised.encode(include_definitions=False)
    assert decode(compact, registry=registry) == revised
    print("\nWire exchange preserves definition revisions, identities, and original values.")
    print("  Inline definitions or resolvable revision identity; local facts require no serialization.")
    compositions(store)
    print("Semantic algebra and runtime behaviors demonstrated in memory.")


if __name__ == "__main__":
    run()
