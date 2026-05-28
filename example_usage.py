"""Usage:
python3 -m examples.example_usage
python3 examples/example_usage.py
"""

import json
import msgpack
import sys
import zlib
from pathlib import Path

if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from occid.schema import *


EXAMPLE_PAYLOAD_VERSION = (1, 0, 0)


def build_example_payload() -> dict:
    rc_link = LinkSchema(
        schema_id="ELRS_915",
        name="ELRS_915",
        link_type=LinkType.POINT_TO_POINT,
        net_type=NetType.RF,
        io=0,
        data_type=LinkDataType.CONTROL,
        addresses=[],
        endpoints=[],
        condition=LinkCondition.GOOD,
    )
    video_link = LinkSchema(
        schema_id="FPV_VIDEO",
        name="FPV_VIDEO",
        link_type=LinkType.POINT_TO_POINT,
        net_type=NetType.RF,
        io=0,
        data_type=LinkDataType.VIDEO,
        addresses=[],
        endpoints=[],
        condition=LinkCondition.GOOD,
    )
    camera = SensorSchema(
        object_type=ObjectType.ENTITY,
        name="NOSE_CAM",
        model="Fixed Camera",
        type=SensorType.EO,
        effect_domain=EffectDomain.AIR,
        max_range=10000.0,
        ptz=False,
        spectrum=SensorSpectrum.VISUAL,
        night_vision=False,
        all_weather=False,
        weather_limits=WeatherLimits(ifr=False),
        error_margin=5.0,
        error_type=SensorErrorType.CEP,
        data_formats=[SensorDataFormat.VIDEO],
        ai=[SensorAICapability.DETECTION],
        datalink="FPV_VIDEO",
    )

    ground_robot = GroundRobot(
        entity_id="robot.ugv.01",
        sys_id="UGV_01",
        alt_ids=[],
        tags=[],
        metadata=[],
        relations=[],
        components=[],
        sensors={},
        model="Tracked Mule",
        role="Ammo carrier",
        status=EntityOperationalState.READY,
        navigation=GroundNavigationSchema(
            propulsion=PropulsionType.TRACKED,
            navigation=NavigationMode.GNSS,
            navaids=[NavAids.GNSS, NavAids.INS],
            max_range=25000.0,
            max_spd=12.0,
        ),
        robot_control=RobotControlSchema(
            control_modes=RobotControlMode.REMOTE,
        ),
        remote_control=RemoteControlSchema(
            links={"RC": rc_link},
            rc_link="ELRS_915",
            channel_map=[],
            mode_ranges=[],
        ),
    )

    air_robot = AirRobot(
        entity_id="air.uav.strike.01",
        sys_id="UAV_STRIKE_01",
        alt_ids=[],
        tags=[],
        metadata=[],
        relations=[],
        components=[],
        model="MK4V2-10",
        status=EntityOperationalState.READY,
        machine_type=MachineType.ROBOT,
        navigation=MilitaryAirNavigation(
            flight_type=AirframeType.COPTER,
            control_modes=[FlightMode.ANGLE, FlightMode.GUIDED],
            failsafe_mode=AirFailsafeMode.RTB,
            weather_limits=WeatherLimits(
                ifr=False,
                wind=NumericRange(max_value=35.0),
                vis=NumericRange(min_value=800.0),
            ),
            roles=[AirRole.GROUND, AirRole.ISR],
            propulsion=PropulsionType.ROTARY_WING,
            navigation=NavigationMode.GNSS,
            navaids=[NavAids.GNSS, NavAids.INS],
            fuel=FuelState(fuel_type=FuelType.BATTERY, capacity=9000.0, remaining=9000.0),
            max_range=10000.0,
            max_flight_t=1200.0,
            max_spd=50.0,
            cruise_spd=35.0,
            max_alt=2000.0,
            start_flight_time=0.0,
        ),
        robot_control=RobotControlSchema(
            control_modes=RobotControlMode.ASSISTED,
            autopilot=True,
            autopilot_controller_model="F405",
            autopilot_type=AutopilotType.INAV,
            autopilot_fw=FirmwareInfo(name="INAV", version=Version(major=8, minor=0, patch=0)),
        ),
        remote_control=RemoteControlSchema(
            links={"RC": rc_link, "VIDEO": video_link},
            rc_link="ELRS_915",
            vid_link="FPV_VIDEO",
            ctrl_video_sep=True,
            channel_map=[],
            mode_ranges=[],
            telemetry=TelemetryState(
                flight_mode=FlightMode.GUIDED,
                battery_pct=100.0,
            ),
        ),
        sensors={"NOSE_CAM": camera},
        maint_status=MaintenanceStatus(state=MaintenanceState.READY),
    )

    ground_org = GroundOrbatOrg(
        org_uid="org.uav.platoon",
        combat_domain=EffectDomain.AIR,
        category=NATOUnitCategory.UAV,
        size=OOBSize.PLT,
        taskforce=False,
        links={},
        tac_elements=[],
        sup_elements=[],
        link_loadout=[
            ItemCount(item_type="ELRS_915", qty=3),
            ItemCount(item_type="FPV_VIDEO", qty=2),
        ],
        tac_e_comp=[
            ItemCount(item_type="robot.ugv.01", qty=1),
            ItemCount(item_type="air.uav.strike.01", qty=2),
        ],
        sup_e_comp=[],
        personnel=[ItemCount(item_type="personnel", qty=6)],
        vehicles=[ItemCount(item_type="pickup", qty=1)],
        equipment=[],
        ammo=[],
        weapons=[],
        air_units=[ItemCount(item_type="air.uav.strike.01", qty=2)],
        spacing=500.0,
    )

    gcs_target = MessageTarget(target_id="gcs")
    uav_target = MessageTarget(target_id="air.uav.strike.01")
    ts_upload = Timestamp(
        seconds=0.0,
        minutes=0.0,
        hours=12.0,
        day=27.0,
        month=5.0,
        year=2026.0,
        tz=-4.0,
    )
    ts_arm = Timestamp(
        seconds=5.0,
        minutes=0.0,
        hours=12.0,
        day=27.0,
        month=5.0,
        year=2026.0,
        tz=-4.0,
    )
    ts_takeoff = Timestamp(
        seconds=10.0,
        minutes=0.0,
        hours=12.0,
        day=27.0,
        month=5.0,
        year=2026.0,
        tz=-4.0,
    )
    ts_telemetry_armed = Timestamp(
        seconds=15.0,
        minutes=0.0,
        hours=12.0,
        day=27.0,
        month=5.0,
        year=2026.0,
        tz=-4.0,
    )
    ts_telemetry_airborne = Timestamp(
        seconds=20.0,
        minutes=0.0,
        hours=12.0,
        day=27.0,
        month=5.0,
        year=2026.0,
        tz=-4.0,
    )

    uav_home = GlobalPosition(
        lat=45.50170,
        lon=-73.56730,
        alt=80.0,
        alt_frame=AltitudeDatum.RELATIVE,
    )
    uav_wp1 = GlobalPosition(
        lat=45.50220,
        lon=-73.56660,
        alt=120.0,
        alt_frame=AltitudeDatum.RELATIVE,
    )
    uav_wp2 = GlobalPosition(
        lat=45.50290,
        lon=-73.56580,
        alt=120.0,
        alt_frame=AltitudeDatum.RELATIVE,
    )
    uav_land = GlobalPosition(
        lat=45.50190,
        lon=-73.56700,
        alt=80.0,
        alt_frame=AltitudeDatum.RELATIVE,
    )
    uav_waypoints = [
        AutopilotMissionWaypoint(waypoint_index=0, position=uav_home),
        AutopilotMissionWaypoint(waypoint_index=1, position=uav_wp1),
        AutopilotMissionWaypoint(waypoint_index=2, position=uav_wp2),
        AutopilotMissionWaypoint(waypoint_index=3, position=uav_land),
    ]
    uav_flight_plan = AutopilotFlightPlan(
        task_id="task.plan.uav-01.flight",
        unit_code="UAV_01",
        assigned_assets=["air.uav.strike.01"],
        status_log=[],
        waypoints=uav_waypoints,
    )
    uav_mission = Mission(
        task_id="task.mission.uav-demo",
        unit_code="UAV_SECTION",
        assigned_assets=["air.uav.strike.01"],
        status_log=[],
        tasks=[uav_flight_plan],
    )

    upload_mission_command = TaskCommand(
        command_id="cmd.upload-mission.001",
        target_ref="air.uav.strike.01",
        task=uav_mission,
    )
    arm_command = VehicleCommand(
        command_id="cmd.arm.001",
        target_ref="air.uav.strike.01",
        command_type=FlightCommandType.ARM,
    )
    takeoff_command = VehicleCommand(
        command_id="cmd.takeoff.001",
        target_ref="air.uav.strike.01",
        command_type=FlightCommandType.TAKEOFF,
    )
    upload_mission_message = CommandMessage(
        msg_id="msg.command.upload-mission.001",
        src=gcs_target,
        dst=uav_target,
        ts=ts_upload,
        priority=MessagePriority.ROUTINE,
        command=upload_mission_command,
    )
    arm_message = CommandMessage(
        msg_id="msg.command.arm.001",
        src=gcs_target,
        dst=uav_target,
        ts=ts_arm,
        priority=MessagePriority.ROUTINE,
        command=arm_command,
    )
    takeoff_message = CommandMessage(
        msg_id="msg.command.takeoff.001",
        src=gcs_target,
        dst=uav_target,
        ts=ts_takeoff,
        priority=MessagePriority.ROUTINE,
        command=takeoff_command,
    )
    telemetry_armed_message = TelemetryMessage(
        msg_id="msg.telemetry.armed.001",
        src=uav_target,
        dst=gcs_target,
        ts=ts_telemetry_armed,
        priority=MessagePriority.ROUTINE,
        state=FlightControlState(
            active_modes=[1],
            active_mode_names=["ARMED"],
        ),
    )
    telemetry_airborne_message = TelemetryMessage(
        msg_id="msg.telemetry.airborne.001",
        src=uav_target,
        dst=gcs_target,
        ts=ts_telemetry_airborne,
        priority=MessagePriority.ROUTINE,
        state=FlightControlState(
            active_modes=[1, 2],
            active_mode_names=["ARMED", "NAV_WP"],
        ),
    )

    return {
        "version": EXAMPLE_PAYLOAD_VERSION,
        "link_templates": [
            link.model_dump(mode="json", exclude_none=True)
            for link in [rc_link, video_link]
        ],
        "ground_robots": [
            ground_robot.model_dump(mode="json", exclude_none=True)
        ],
        "air_robots": [
            air_robot.model_dump(mode="json", exclude_none=True)
        ],
        "ground_orgs": [
            ground_org.model_dump(mode="json", exclude_none=True)
        ],
        "uav_waypoints": [
            waypoint.model_dump(mode="json", exclude_none=True)
            for waypoint in uav_waypoints
        ],
        "uav_flight_plan": uav_flight_plan.model_dump(mode="json", exclude_none=True),
        "uav_mission": uav_mission.model_dump(mode="json", exclude_none=True),
        "uav_commands": [
            command.model_dump(mode="json", exclude_none=True)
            for command in [upload_mission_command, arm_command, takeoff_command]
        ],
        "command_messages": [
            message.model_dump(mode="json", exclude_none=True)
            for message in [upload_mission_message, arm_message, takeoff_message]
        ],
        "telemetry_messages": [
            message.model_dump(mode="json", exclude_none=True)
            for message in [telemetry_armed_message, telemetry_airborne_message]
        ],
    }


def roundtrip_payload(payload: dict) -> dict:
    payload_json = json.dumps(payload, separators=(",", ":")).encode()
    packed_json = zlib.compress(payload_json, level=6)
    payload_msgpack = msgpack.packb(payload, use_bin_type=True)
    packed_msgpack = zlib.compress(payload_msgpack, level=6)
    unpacked_json = json.loads(zlib.decompress(packed_json))
    unpacked_msgpack = msgpack.unpackb(zlib.decompress(packed_msgpack), raw=False)

    unpacked_links = [
        LinkSchema.model_validate(link_payload)
        for link_payload in unpacked_json["link_templates"]
    ]
    unpacked_ground_robots = [
        GroundRobot.model_validate(robot_payload)
        for robot_payload in unpacked_json["ground_robots"]
    ]
    unpacked_air_robots = [
        AirRobot.model_validate(machine_payload)
        for machine_payload in unpacked_json["air_robots"]
    ]
    unpacked_ground_orgs = [
        GroundOrbatOrg.model_validate(org_payload)
        for org_payload in unpacked_json["ground_orgs"]
    ]
    unpacked_uav_waypoints = [
        AutopilotMissionWaypoint.model_validate(waypoint_payload)
        for waypoint_payload in unpacked_json["uav_waypoints"]
    ]
    unpacked_uav_flight_plan = AutopilotFlightPlan.model_validate(unpacked_json["uav_flight_plan"])
    unpacked_uav_mission = Mission.model_validate(unpacked_json["uav_mission"])
    unpacked_uav_commands = [
        TaskCommand.model_validate(unpacked_json["uav_commands"][0]),
        VehicleCommand.model_validate(unpacked_json["uav_commands"][1]),
        VehicleCommand.model_validate(unpacked_json["uav_commands"][2]),
    ]
    unpacked_command_messages = [
        CommandMessage.model_validate(message_payload)
        for message_payload in unpacked_json["command_messages"]
    ]
    unpacked_telemetry_messages = [
        TelemetryMessage.model_validate(message_payload)
        for message_payload in unpacked_json["telemetry_messages"]
    ]

    unpacked_msgpack_links = [
        LinkSchema.model_validate(link_payload)
        for link_payload in unpacked_msgpack["link_templates"]
    ]
    unpacked_msgpack_ground_robots = [
        GroundRobot.model_validate(robot_payload)
        for robot_payload in unpacked_msgpack["ground_robots"]
    ]
    unpacked_msgpack_air_robots = [
        AirRobot.model_validate(machine_payload)
        for machine_payload in unpacked_msgpack["air_robots"]
    ]
    unpacked_msgpack_ground_orgs = [
        GroundOrbatOrg.model_validate(org_payload)
        for org_payload in unpacked_msgpack["ground_orgs"]
    ]
    unpacked_msgpack_uav_waypoints = [
        AutopilotMissionWaypoint.model_validate(waypoint_payload)
        for waypoint_payload in unpacked_msgpack["uav_waypoints"]
    ]
    print(unpacked_msgpack_uav_waypoints)
    for i in unpacked_msgpack_uav_waypoints:
        print(i)
    unpacked_msgpack_uav_flight_plan = AutopilotFlightPlan.model_validate(unpacked_msgpack["uav_flight_plan"])
    unpacked_msgpack_uav_mission = Mission.model_validate(unpacked_msgpack["uav_mission"])
    unpacked_msgpack_uav_commands = [
        TaskCommand.model_validate(unpacked_msgpack["uav_commands"][0]),
        VehicleCommand.model_validate(unpacked_msgpack["uav_commands"][1]),
        VehicleCommand.model_validate(unpacked_msgpack["uav_commands"][2]),
    ]
    unpacked_msgpack_command_messages = [
        CommandMessage.model_validate(message_payload)
        for message_payload in unpacked_msgpack["command_messages"]
    ]
    unpacked_msgpack_telemetry_messages = [
        TelemetryMessage.model_validate(message_payload)
        for message_payload in unpacked_msgpack["telemetry_messages"]
    ]

    return {
        "payload_json": payload_json,
        "packed_json": packed_json,
        "payload_msgpack": payload_msgpack,
        "packed_msgpack": packed_msgpack,
        "unpacked_links": unpacked_links,
        "unpacked_ground_robots": unpacked_ground_robots,
        "unpacked_air_robots": unpacked_air_robots,
        "unpacked_ground_orgs": unpacked_ground_orgs,
        "unpacked_msgpack_links": unpacked_msgpack_links,
        "unpacked_msgpack_ground_robots": unpacked_msgpack_ground_robots,
        "unpacked_msgpack_air_robots": unpacked_msgpack_air_robots,
        "unpacked_msgpack_ground_orgs": unpacked_msgpack_ground_orgs,
        "unpacked_uav_waypoints": unpacked_uav_waypoints,
        "unpacked_uav_flight_plan": unpacked_uav_flight_plan,
        "unpacked_uav_mission": unpacked_uav_mission,
        "unpacked_uav_commands": unpacked_uav_commands,
        "unpacked_command_messages": unpacked_command_messages,
        "unpacked_telemetry_messages": unpacked_telemetry_messages,
        "unpacked_msgpack_uav_waypoints": unpacked_msgpack_uav_waypoints,
        "unpacked_msgpack_uav_flight_plan": unpacked_msgpack_uav_flight_plan,
        "unpacked_msgpack_uav_mission": unpacked_msgpack_uav_mission,
        "unpacked_msgpack_uav_commands": unpacked_msgpack_uav_commands,
        "unpacked_msgpack_command_messages": unpacked_msgpack_command_messages,
        "unpacked_msgpack_telemetry_messages": unpacked_msgpack_telemetry_messages,
    }


def main() -> None:
    payload = build_example_payload()
    roundtrip = roundtrip_payload(payload)

    print(json.dumps(payload, indent=2))
    print()
    print(f"json_bytes={len(roundtrip['payload_json'])}")
    print(f"json_zlib_bytes={len(roundtrip['packed_json'])}")
    print(f"msgpack_bytes={len(roundtrip['payload_msgpack'])}")
    print(f"msgpack_zlib_bytes={len(roundtrip['packed_msgpack'])}")
    print(f"unpacked_links={[link.schema_id for link in roundtrip['unpacked_links']]}")
    print(
        f"unpacked_ground_robots={[robot.entity_id for robot in roundtrip['unpacked_ground_robots']]}"
    )
    print(
        f"unpacked_air_robots={[machine.entity_id for machine in roundtrip['unpacked_air_robots']]}"
    )
    print(
        f"unpacked_ground_orgs={[org.org_uid for org in roundtrip['unpacked_ground_orgs']]}"
    )
    print(
        f"unpacked_uav_waypoints={[waypoint.waypoint_index for waypoint in roundtrip['unpacked_uav_waypoints']]}"
    )
    print(f"unpacked_uav_flight_plan={roundtrip['unpacked_uav_flight_plan'].task_id}")
    print(
        f"unpacked_uav_mission_tasks={[task.task_id for task in roundtrip['unpacked_uav_mission'].tasks]}"
    )
    print(
        f"unpacked_command_messages={[message.msg_id for message in roundtrip['unpacked_command_messages']]}"
    )
    print(
        f"unpacked_telemetry_messages={[message.msg_id for message in roundtrip['unpacked_telemetry_messages']]}"
    )
    print(
        f"unpacked_msgpack_ground_robots={[robot.entity_id for robot in roundtrip['unpacked_msgpack_ground_robots']]}"
    )
    print(
        f"unpacked_msgpack_air_robots={[machine.entity_id for machine in roundtrip['unpacked_msgpack_air_robots']]}"
    )
    print(
        f"unpacked_msgpack_ground_orgs={[org.org_uid for org in roundtrip['unpacked_msgpack_ground_orgs']]}"
    )
    print(
        f"unpacked_msgpack_uav_waypoints={[waypoint.waypoint_index for waypoint in roundtrip['unpacked_msgpack_uav_waypoints']]}"
    )
    print(f"unpacked_msgpack_uav_flight_plan={roundtrip['unpacked_msgpack_uav_flight_plan'].task_id}")
    print(
        f"unpacked_msgpack_uav_mission_tasks={[task.task_id for task in roundtrip['unpacked_msgpack_uav_mission'].tasks]}"
    )
    print(
        f"unpacked_msgpack_command_messages={[message.msg_id for message in roundtrip['unpacked_msgpack_command_messages']]}"
    )
    print(
        f"unpacked_msgpack_telemetry_messages={[message.msg_id for message in roundtrip['unpacked_msgpack_telemetry_messages']]}"
    )


if __name__ == "__main__":
    main()
