"""Executable semantic algebra, live extension, and durable observation demo."""
from pathlib import Path
import tempfile

from occid2 import (
    AmbiguousSemanticMatch, IllegalSemanticCombination, decode, new_store, sem,
)


def run(database: Path) -> None:
    with new_store(database) as store:
        registry = store.registry
        Position = registry.product("Position")
        Representation = registry.axis("Representation")
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
            Position * Representation.Geodetic,
            {"lat": 36.530440, "lon": -83.216383, "h": 125.0},
            source={"protocol": "MAVLink", "representation": "chart-unit position observation"},
            observed_at="2026-10-10T12:00:00Z",
            provenance={"kind": "observation", "reference": "WGS84 ellipsoid"},
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
        opaque = uav.set("Unresolved.SensorQuantity", {"native": b"\x01\x02", "unknown": None}, source="future sensor")
        assert uav.get("Unresolved.SensorQuantity") == opaque

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
        answer = target.set(Position * Representation.Geodetic, {"lat": 36.530440, "lon": -83.216383, "h": 90.0}, source="target sensor")
        assert locate.solve()["position"] == answer
        print("\nOpen expressions keep typed unknowns and solve when facts arrive.")
        print(" ", move)
        print(" ", locate, "->", locate.solve()["position"].value)
        assignment = store.relate("AssignedWork", assignee=uav, work=move.ref)
        assert assignment.roles["assignee"].uid == "uav-1"
        assert assignment in store.relations("Directed")
        try:
            store.relate("AssignedWork", assignee=move.ref, work=uav)
        except TypeError:
            print("  Directed roles validated:", assignment)
        else:
            raise AssertionError("reversed assignment must be rejected")

        another = uav.set(Position * Representation.Geodetic, {"lat": 36.530440, "lon": -83.216383, "h": 126.0}, source="second sensor", observed_at="2026-10-10T12:00:03Z", provenance={"reference": "WGS84 ellipsoid"})
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

        registry.update({"mappings": {"position-report": {"semantics": ["Position", "Representation.Geodetic"], "fields": {"lat": "latitude", "lon": "longitude", "h": "ellipsoid_height"}, "context": {"reference": "WGS84 ellipsoid", "units": {"latitude": "deg", "longitude": "deg", "ellipsoid_height": "m"}}}}})
        report = store.ref("report-subject", "Entity")
        raw = report.set(sem(), {"latitude": 36.530440, "longitude": -83.216383, "ellipsoid_height": 125.0, "msl_height": 110.0, "unknown_source_field": b"\xff\x00"}, source="external position report", observed_at=1234)
        mapped = store.interpret(raw, "position-report")
        registry.update({"mappings": {"position-report": {"semantics": ["Position", "Representation.Geodetic"], "fields": {"lat": "latitude", "lon": "longitude", "h": "msl_height"}, "context": {"reference": "MSL", "units": {"latitude": "deg", "longitude": "deg", "msl_height": "m"}}}}})
        revised = store.interpret(raw, "position-report")
        assert mapped.value["h"] == 125.0 and revised.value["h"] == 110.0
        assert mapped.definition_id != revised.definition_id
        assert mapped.provenance["derived_from"] == revised.provenance["derived_from"] == [raw.id]
        print("\nMapping revision creates a new interpretation and retains the complete source report.")
        identities = [datum.id for datum in uav.find(Position)]
        raw_value = raw.value
        current_revision = registry.definition_id

    with new_store(database) as restored:
        uav = restored.ref("uav-1")
        assert [datum.id for datum in uav.find("Position")] == identities
        assert restored.registry.definition_id == current_revision
        assert restored.expression("task-move-1").unbound == []
        assert restored.expression("task-locate-1").solve()["position"].value["h"] == 90.0
        assert restored.relations("AssignedWork")[0].roles["work"].uid == "task-move-1"
        report = restored.ref("report-subject")
        assert report.find()[0].value == raw_value
        assert [datum.value["h"] for datum in report.find("Position")] == [125.0, 110.0]
        assert report.find("Position")[0].provenance["context"]["reference"] == "WGS84 ellipsoid"
        assert restored.registry.axis("Representation").Polar
        print("\nSQLite reopen preserves definitions, identities, original values, bindings, and relation roles.")
        print("All 14 architecture acceptance behaviors demonstrated.")


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        run(Path(directory) / "occid2.sqlite")


if __name__ == "__main__":
    main()
