from runtime import sem, value_semantics
from generated.occid2 import (
    Actor,
    AirMission,
    AirTask,
    Airframe,
    Altitude,
    Biological,
    BloodGroup,
    Controller,
    Destination,
    PhysicalDomain,
    Drone,
    EffectIntent,
    Frame,
    GlobalPosition,
    InformationIntent,
    Machine,
    ManeuverIntent,
    Mark,
    Mission,
    Person,
    Position,
    Target,
    TaskEffect,
    TaskInformation,
    TaskManeuver,
    UAV,
    UnmannedVehicle,
    new_store,
)


def main() -> None:
    store = new_store()
    registry = store.registry

    uav = store.ref("uav-1", UnmannedVehicle)
    mark = store.ref("mark-alpha", Mark)

    gp = GlobalPosition(lat=45.30, lon=-74.20, alt_m=125.0)
    uav.set(gp)
    mark.set(Mark(uid="mark-alpha", name="alpha"))

    print("Aliases are products, not classes:")
    print("  Drone      =", Drone)
    print("  UAV        =", UAV)
    print("  AirMission =", AirMission)
    print("  Drone == UAV × Airframe.MULTIROTOR:", Drone == sem(UAV, Airframe.MULTIROTOR))
    print()

    print("Exact and semantic lookup:")
    print("  exact GlobalPosition:", uav.get(GlobalPosition))
    print("  semantic Position   :", uav.get(Position, Frame.WGS84))
    print("  Mark answers Position:", [type(x).__name__ for x in mark.find(Position)])
    print()

    move_value = TaskManeuver(
        uid="task-move-1",
        instruction="move to mark alpha",
        intent=ManeuverIntent.MOVE,
    )
    move = store.ref(move_value.uid, TaskManeuver)
    move.set(move_value)

    print("MOVE surface vocabulary entails:")
    print(" ", value_semantics(move_value))
    print()

    locate_value = TaskInformation(
        uid="task-locate-1",
        instruction="locate uav-1",
        intent=InformationIntent.LOCATE,
    )
    print("LOCATE surface vocabulary entails:")
    print(" ", value_semantics(locate_value))
    print()

    create_value = TaskEffect(
        uid="task-create-1",
        instruction="make the object exist",
        intent=EffectIntent.CREATE,
    )
    print("CREATE surface vocabulary entails:")
    print(" ", value_semantics(create_value))
    print()

    print("Relations are directed, operands validated semantically:")
    store.relate(Destination, move, mark)
    store.relate(Target, move, uav)
    for relation in store.relations():
        print(" ", relation)
    print()

    print("Legality from declared constraints:")
    print("  Drone × BloodGroup.A_POS:", registry.legal(sem(Drone, BloodGroup.A_POS)))
    print("  Machine × Actor:", registry.legal(sem(Machine, Actor)))
    print("  Mission × PhysicalDomain.AIR × Altitude:", registry.legal(sem(Mission, PhysicalDomain.AIR, Altitude)))
    print("  Mission × PhysicalDomain.SEA × Altitude:", registry.legal(sem(Mission, PhysicalDomain.SEA, Altitude)))
    print()

    print("Emergent applicability:")
    print("  AirTask = Task × AIR gains Altitude:", registry.applicable(AirTask, Altitude))
    print()

    print("Codeword-opened relations:")
    print("  MOVE  ->", registry.codeword_relation(ManeuverIntent.MOVE))
    print("  LOCATE ->", registry.codeword_relation(InformationIntent.LOCATE))
    print()

    print("Derived entailment:")
    print(
        "  Drone entails Machine × Controller.UNMANNED × PhysicalDomain.AIR:",
        registry.entails(Drone, sem(Machine, Controller.UNMANNED, PhysicalDomain.AIR)),
    )
    print("  Person entails Biological:", registry.entails(sem(Person), Biological))


if __name__ == "__main__":
    main()
