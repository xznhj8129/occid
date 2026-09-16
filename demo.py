from runtime import sem, value_semantics
from generated.occid2 import (
    BloodGroup,
    Destination,
    Domain,
    Drone,
    EffectIntent,
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


def main() -> None:
    store = new_store()

    drone = store.ref("drone-1", Drone)
    rover = store.ref("rover-1", GroundRobot)
    mark = store.ref("mark-alpha", Mark)

    drone.set(GlobalPosition(lat=45.30, lon=-74.20, alt_m=125.0))
    rover.set(GlobalPosition(lat=45.31, lon=-74.22, alt_m=2.0))

    print("Drone semantics:")
    print(" ", Drone._semantics)
    print()

    print("Semantic position query:")
    print(" ", drone.get(Position, Frame.WGS84))
    print()

    print("Exact representation query:")
    print(" ", drone.get(GlobalPosition))
    print()

    move_value = TaskManeuver(
        uid="task-move-1",
        instruction="move to mark alpha",
        intent=ManeuverIntent.MOVE,
    )
    move = store.ref(move_value.uid, TaskManeuver)
    move.set(move_value)
    store.relate(Destination, move, mark)

    print("MOVE surface vocabulary expands to:")
    print(" ", value_semantics(move_value))
    print()

    locate_value = TaskInformation(
        uid="task-locate-1",
        instruction="locate rover-1",
        intent=InformationIntent.LOCATE,
    )
    locate = store.ref(locate_value.uid, TaskInformation)
    locate.set(locate_value)

    print("LOCATE surface vocabulary expands to:")
    print(" ", value_semantics(locate_value))
    print()

    create_value = TaskEffect(
        uid="task-create-1",
        instruction="make the required object exist",
        intent=EffectIntent.CREATE,
    )
    print("CREATE surface vocabulary expands to:")
    print(" ", value_semantics(create_value))
    print()

    print("Semantic discovery on the MOVE task:")
    print(" ", [type(x).__name__ for x in move.find(Position)])
    print()

    print("Relations:")
    for relation in store.relations():
        print(" ", relation)
    print()

    print("Legality:")
    print("  Drone × Domain.LAND:", store.registry.legal(sem(Drone, Domain.LAND)))
    print("  Drone × BloodGroup.A_POS:", store.registry.legal(sem(Drone, BloodGroup.A_POS)))
    print("  Person × BloodGroup.A_POS:", store.registry.legal(sem(Person, BloodGroup.A_POS)))

    print()
    print("Human-readable equivalence:")
    print(
        "  MOVE == Task × WORLD × ACHIEVE × Position:",
        store.registry.equivalent(
            ManeuverIntent.MOVE._semantics,
            sem(Task, Realm.WORLD, TemporalMode.ACHIEVE, Position),
        ),
    )


if __name__ == "__main__":
    main()
