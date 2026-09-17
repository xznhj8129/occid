from dataclasses import fields

from runtime import sem
from generated.occid2 import (
    Actor,
    Airframe,
    Altitude,
    AssignedWork,
    BloodGroup,
    Controller,
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
    PhysicalDomain,
    Position,
    Representation,
    TaskInformation,
    TaskManeuver,
    UAV,
    UnmannedVehicle,
    VehicleState,
    new_store,
)


def main() -> None:
    store = new_store()
    registry = store.registry

    print("A semantic object is a product; an alias is only a name.")
    print("  Drone      =", Drone)
    print("  Drone == UAV * Airframe.MULTIROTOR:", Drone == sem(UAV, Airframe.MULTIROTOR))
    print("  Geodetic == Representation.Geodetic:", Geodetic == sem(Representation.Geodetic))
    print()

    print("A chart reduces a quantity in a representation to irreducible variables.")
    for chart in registry.charts:
        print(f"   {chart}")
    print("  GlobalPosition:", [field.name for field in fields(GlobalPosition)])
    print("  VehicleState  :", [field.name for field in fields(VehicleState)])
    print("  VehicleState units:", dict(VehicleState._units))
    print()

    print("Data is stored in a representation and addressed by meaning.")
    uav = store.ref("uav-1", UnmannedVehicle)
    uav.set(GlobalPosition(lat=45.30, lon=-74.20, h=125.0))
    uav.set(LocalPosition(x=120.0, y=-40.0, z=15.0))
    print("  uav * Position            ->", [type(x).__name__ for x in uav.find(Position)])
    print("  uav * Position * Geodetic ->", uav.get(Position, Representation.Geodetic))
    print("  uav * Position * Local    ->", uav.get(Position, Representation.LocalCartesian))
    print()

    print("A projection is the compiled normal form of chart-selected facts.")
    uav.set(LocalVelocity(vx=12.0, vy=0.0, vz=-1.5))
    uav.set(LocalAttitude(roll=0.0, pitch=0.0, yaw=1.57))
    print(f"   {store.project(uav, VehicleState)}")
    print()

    print("A task is an open expression: fixed factors + typed free variables.")
    print("  MOVE =", MOVE)
    move = store.task(
        "task-move-1",
        TaskManeuver,
        ManeuverIntent.MOVE,
        instruction="move to mark alpha",
    )
    print("  fixed semantics:", move.factors)
    print(f"   {move}")
    move.bind("actor", uav)
    print(f"   {move}")
    mark = store.ref("mark-alpha", Mark)
    mark.set(Mark(uid="mark-alpha", name="alpha", lat=45.28, lon=-74.18, h=110.0))
    move.bind("destination", mark)
    print(f"   {move} unbound: {move.unbound}")
    print()

    print("An unbound variable is an unknown, not an error.")
    target = store.ref("target-42", UnmannedVehicle)
    locate = store.task(
        "task-locate-1",
        TaskInformation,
        InformationIntent.LOCATE,
        instruction="locate target-42",
    )
    locate.bind("target", target)
    print(f"   {locate}")
    print(f"   no position fact yet -> solve() = {locate.solve()}")
    target.set(GlobalPosition(lat=45.10, lon=-74.40, h=90.0))
    print(f"   fact arrives         -> solve() = {locate.solve()}")
    print()

    print("Relations connect independent things; roles belong to the relation.")
    store.relate(AssignedWork, uav, move.ref)
    for fact in store.relations(Directed):
        print(f"   {fact}")
    print()

    print("Legality is derived from declared constraints, never enumerated.")
    print("  Drone * BloodGroup.A_POS :", registry.legal(sem(Drone, BloodGroup.A_POS)))
    print("  Machine * Actor          :", registry.legal(sem(Machine, Actor)))
    print("  Mission * AIR * Altitude :", registry.legal(sem(Mission, PhysicalDomain.AIR, Altitude)))
    print("  Mission * SEA * Altitude :", registry.legal(sem(Mission, PhysicalDomain.SEA, Altitude)))
    print(
        "  Drone entails Machine * Controller.UNMANNED * AIR:",
        registry.entails(Drone, sem(Machine, Controller.UNMANNED, PhysicalDomain.AIR)),
    )


if __name__ == "__main__":
    main()
