"""Usage:
python3 -m examples.example_usage
python3 examples/example_usage.py
"""

import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from occid.schema import *


def main() -> None:
    EXAMPLE_PAYLOAD_VERSION = (1, 0, 0)
    EXAMPLE_ID_TYPE = IdentifierType.DB_ID

    def record_meta(record_id: str, timestamp: float = 0.0) -> RecordMeta:
        return RecordMeta(
            record_id=StringID(id_type=EXAMPLE_ID_TYPE, value=record_id),
            created_ts=timestamp,
            updated_ts=timestamp,
            origin_system="occid.example",
            provenance=[],
        )
    rc_link = Link(
        schema_id=StringID(id_type=EXAMPLE_ID_TYPE, value="ELRS_915"),
        name="ELRS_915",
        link_type=LinkType.POINT_TO_POINT,
        net_type=NetType.RF,
        data_type=LinkDataType.CONTROL,
        condition=LinkCondition.GOOD,
    )
    video_link = Link(
        schema_id=StringID(id_type=EXAMPLE_ID_TYPE, value="FPV_VIDEO"),
        name="FPV_VIDEO",
        link_type=LinkType.POINT_TO_POINT,
        net_type=NetType.RF,
        data_type=LinkDataType.VIDEO,
        condition=LinkCondition.GOOD,
    )
    camera = ImageSensor(
        name="NOSE_CAM",
        model="Fixed Camera",
        type=SensorType.EO,
        serial_uid=StringID(id_type=EXAMPLE_ID_TYPE, value="sensor.nose-cam.serial"),
        effect_domain=EffectDomain.AIR,
        max_range=10000.0,
        ptz=False,
        spectrum=SensorSpectrum.VISUAL,
        all_weather=False,
        weather_limits=WeatherLimits(ifr=False),
        error_margin=5.0,
        error_type=SensorErrorType.CEP,
        data_formats=[SensorDataFormat.VIDEO],
        ai=[SensorAICapability.DETECTION],
        night_vision=False,
    )

    ground_node = Node(
        node_id=StringID(id_type=EXAMPLE_ID_TYPE, value="node.ugv.01"),
        entity_id=StringID(id_type=EXAMPLE_ID_TYPE, value="robot.ugv.01"),
        roles=[CapabilityRole.EFFECTOR],
        addresses=[],
        links={"RC": rc_link},
        radios={},
        protocols={},
    )
    uav_node = Node(
        node_id=StringID(id_type=EXAMPLE_ID_TYPE, value="node.uav01"),
        entity_id=StringID(id_type=EXAMPLE_ID_TYPE, value="air.uav01"),
        roles=[CapabilityRole.EFFECTOR, CapabilityRole.SENSOR],
        addresses=[],
        links={"RC": rc_link, "VIDEO": video_link},
        radios={},
        protocols={},
    )

    ground_robot = GroundRobot(
        record=record_meta("record.robot.ugv.01"),
        entity_id=StringID(id_type=EXAMPLE_ID_TYPE, value="robot.ugv.01"),
        node_ids=[ground_node.node_id],
        sys_id=StringID(id_type=EXAMPLE_ID_TYPE, value="UGV_01"),
        propulsion=PropulsionType.TRACKED,
        alt_ids=[],
        tags=[],
        metadata={},
        relations=[],
        components=[],
        serial_uid=StringID(id_type=EXAMPLE_ID_TYPE, value="robot.ugv.01.serial"),
        sensors={},
        model="Tracked Mule",
        role="Ammo carrier",
        navigation=GroundNavigationSchema(
            propulsion=PropulsionType.TRACKED,
            navigation=NavigationMode.GNSS,
            navaids=[NavAids.GNSS, NavAids.INS],
            max_range=25000.0,
            max_spd=12.0,
        ),
    )

    air_robot = Drone(
        record=record_meta("record.air.uav01"),
        entity_id=StringID(id_type=EXAMPLE_ID_TYPE, value="air.uav01"),
        node_ids=[uav_node.node_id],
        sys_id=StringID(id_type=EXAMPLE_ID_TYPE, value="UAV01"),
        propulsion=PropulsionType.ROTARY_WING,
        alt_ids=[],
        tags=[],
        metadata={},
        relations=[],
        components=[],
        serial_uid=StringID(id_type=EXAMPLE_ID_TYPE, value="air.uav01.serial"),
        model="MK4V2-10",
        machine_type=MachineType.ROBOT,
        navigation=AirNavigationSchema(
            flight_type=AirframeType.COPTER,
            control_modes=[FlightMode.ANGLE, FlightMode.GUIDED],
            failsafe_mode=AirFailsafeMode.RTB,
            weather_limits=WeatherLimits(
                ifr=False,
                wind=NumericRange(max_value=35.0),
                vis=NumericRange(min_value=800.0),
            ),
            propulsion=PropulsionType.ROTARY_WING,
            navigation=NavigationMode.GNSS,
            navaids=[NavAids.GNSS, NavAids.INS],
            max_range=10000.0,
            max_flight_t=1200.0,
            max_spd=50.0,
            cruise_spd=35.0,
            max_alt=2000.0,
        ),
        controller=RobotController(
            control_modes=RobotControlMode.ASSISTED,
            autopilot_type=AutopilotType.INAV,
            autopilot_firmware=FirmwareInfo(name="INAV", version=Version(major=8, minor=0, patch=0)),
        ),
        remote_control=RemoteControlSchema(
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
    )

    ground_org = GroundOrbatOrg(
        record=record_meta("record.org.uav.platoon"),
        org_uid=StringID(id_type=EXAMPLE_ID_TYPE, value="org.uav.platoon"),
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
            ItemCount(item_type="air.uav01", qty=2),
        ],
        sup_e_comp=[],
        personnel=[ItemCount(item_type="personnel", qty=6)],
        vehicles=[ItemCount(item_type="pickup", qty=1)],
        equipment=[],
        ammo=[],
        weapons=[],
        air_units=[ItemCount(item_type="air.uav01", qty=2)],
        spacing=500.0,
    )

    gcs_target = MessageTarget(target_id=StringID(id_type=EXAMPLE_ID_TYPE, value="gcs"))
    uav_target = MessageTarget(target_id=StringID(id_type=EXAMPLE_ID_TYPE, value="air.uav01"))
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
        lat=36.530440,
        lon=-83.216383,
        alt=80.0,
        alt_frame=AltitudeDatum.RELATIVE,
    )
    uav_wp1 = GlobalPosition(
        lat=36.531040,
        lon=-83.215683,
        alt=120.0,
        alt_frame=AltitudeDatum.RELATIVE,
    )
    uav_wp2 = GlobalPosition(
        lat=36.531640,
        lon=-83.214983,
        alt=120.0,
        alt_frame=AltitudeDatum.RELATIVE,
    )
    uav_land = GlobalPosition(
        lat=36.530640,
        lon=-83.216083,
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
        record=record_meta("record.plan.uav-01.flight"),
        plan_id=StringID(id_type=EXAMPLE_ID_TYPE, value="plan.uav-01.flight"),
        objective_ids=[],
        task_ids=[StringID(id_type=EXAMPLE_ID_TYPE, value="task.mission.uav-demo")],
        actor_ids=[air_robot.entity_id],
        resource_ids=[],
        assignments=[],
        steps=[],
        routes=[],
        constraints=[],
        contingencies=[],
        waypoints=uav_waypoints,
    )
    uav_mission = Mission(
        record=record_meta("record.task.mission.uav-demo"),
        task_id=StringID(id_type=EXAMPLE_ID_TYPE, value="task.mission.uav-demo"),
        tasks=[],
    )

    upload_mission_command = ApplyPlanCommand(
        plan=uav_flight_plan,
    )

    arm_command = ArmCommand()
    takeoff_command = TakeoffCommand()
    upload_mission_message = CommandMessage(
        src=gcs_target,
        dst=uav_target,
        ts=ts_upload,
        priority=MessagePriority.ROUTINE,
        seq=1,
        command=upload_mission_command,
    )
    arm_message = CommandMessage(
        src=gcs_target,
        dst=uav_target,
        ts=ts_arm,
        priority=MessagePriority.ROUTINE,
        seq=2,
        command=arm_command,
    )
    takeoff_message = CommandMessage(
        src=gcs_target,
        dst=uav_target,
        ts=ts_takeoff,
        priority=MessagePriority.ROUTINE,
        seq=3,
        command=takeoff_command,
    )
    telemetry_armed_message = UAVTelemetryMessage(
        src=uav_target,
        dst=gcs_target,
        ts=ts_telemetry_armed,
        priority=MessagePriority.ROUTINE,
        seq=4,
        state=TelemetryState(
            flight_mode=FlightMode.GUIDED,
            battery_pct=99.0,
        ),
    )
    telemetry_airborne_message = UAVTelemetryMessage(
        src=uav_target,
        dst=gcs_target,
        ts=ts_telemetry_airborne,
        priority=MessagePriority.ROUTINE,
        seq=5,
        state=TelemetryState(
            flight_mode=FlightMode.NAV_WP,
            flight_phase=FlightPhase.CRUISE,
            battery_pct=98.0,
        ),
    )

    print()
    upload_mission_encoded = upload_mission_message.encode()
    upload_mission_decoded = CommandMessage.decode(upload_mission_encoded)
    print(upload_mission_message)
    print("SEQ:", upload_mission_decoded.seq)
    print("TARGET:", upload_mission_decoded.dst.target_id.value)
    print("SIZE:", len(upload_mission_encoded))
    for waypoint in upload_mission_decoded.command.plan.waypoints:
        print(
            "WAYPOINT:",
            waypoint.waypoint_index,
            waypoint.position.lat,
            waypoint.position.lon,
            waypoint.position.alt,
            waypoint.position.alt_frame,
        )

    print()
    arm_encoded = arm_message.encode()
    arm_decoded = CommandMessage.decode(arm_encoded)
    print(arm_message)
    print("SEQ:", arm_decoded.seq)
    print("TARGET:", arm_decoded.dst.target_id.value)
    print("SIZE:", len(arm_encoded))

    print()
    takeoff_encoded = takeoff_message.encode()
    takeoff_decoded = CommandMessage.decode(takeoff_encoded)
    print(takeoff_message)
    print("SEQ:", takeoff_decoded.seq)
    print("TARGET:", takeoff_decoded.dst.target_id.value)
    print("SIZE:", len(takeoff_encoded))

    print()
    telemetry_armed_encoded = telemetry_armed_message.encode()
    telemetry_armed_decoded = UAVTelemetryMessage.decode(telemetry_armed_encoded)
    print("SEQ:", telemetry_armed_decoded.seq)
    print("MODE:", telemetry_armed_decoded.state.flight_mode.name)
    print("BATTERY:", telemetry_armed_decoded.state.battery_pct)
    print("SIZE:", len(telemetry_armed_encoded))

    print()
    telemetry_airborne_encoded = telemetry_airborne_message.encode()
    telemetry_airborne_decoded = UAVTelemetryMessage.decode(telemetry_airborne_encoded)
    print("SEQ:", telemetry_airborne_decoded.seq)
    print("MODE:", telemetry_airborne_decoded.state.flight_mode.name)
    print("PHASE:", telemetry_airborne_decoded.state.flight_phase.name)
    print("BATTERY:", telemetry_airborne_decoded.state.battery_pct)
    print("SIZE:", len(telemetry_airborne_encoded))


if __name__ == "__main__":
    main()
