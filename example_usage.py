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
        condition=LinkCondition.GOOD,
    )
    video_link = LinkSchema(
        schema_id="FPV_VIDEO",
        name="FPV_VIDEO",
        link_type=LinkType.POINT_TO_POINT,
        net_type=NetType.RF,
        io=0,
        data_type=LinkDataType.VIDEO,
        condition=LinkCondition.GOOD,
    )
    camera = SensorSchema(
        name="NOSE_CAM",
        model="Fixed Camera",
        type=SensorType.EO,
        effect_domain=EffectDomain.AIR,
        max_range=10000.0,
        ptz=False,
        spectrum=SensorSpectrum.VISUAL,
        night_vision=False,
        all_weather=False,
        error_margin=5.0,
        error_type=SensorErrorType.CEP,
        datalink="FPV_VIDEO",
    )

    payload_common = PayloadSchema(
        item_type=PayloadType.WEAPON,
        weapons=[ItemCount(item_type="PG7V", qty=1)],
        ammo=[ItemCount(item_type="PG7V", qty=1)],
        ordnance=[ItemCount(item_type="PG7V", qty=1)],
        payload_mounts={
            "center": PayloadMountSchema(
                mount_id="center",
                item_id="payload.pg7v",
                qty=1,
                launcher="hand",
                compat_tags=[PayloadType.WEAPON],
                loaded=[PayloadAllocation(payload_type=PayloadType.WEAPON, qty=1)],
            )
        },
        payload_plan=PayloadPlanSchema(
            requested=[PayloadAllocation(payload_type=PayloadType.WEAPON, qty=1)],
            approved=[PayloadAllocation(payload_type=PayloadType.WEAPON, qty=1)],
            loaded=[PayloadAllocation(payload_type=PayloadType.WEAPON, qty=1)],
            notes="single-shot strike payload",
        ),
    )

    ground_robot = GroundRobot(
        entity_id="robot.ugv.01",
        sys_id="UGV_01",
        model="Tracked Mule",
        role="Ammo carrier",
        status=EntityOperationalState.READY,
        payload=PayloadSchema(
            item_type=PayloadType.CARGO,
            ammo=[ItemCount(item_type="7.62x54R", qty=800)],
            ordnance=[ItemCount(item_type="smoke", qty=4)],
        ),
        effects=GroundEffectsSchema(
            has_launchers=False,
            payload_mounts={},
            effect_domain=EffectDomain.LAND,
            launch_domain=OperationalDomain.LAND,
            guidance=GuidanceType.UNGUIDED,
            warhead=WarheadType.INERT,
            attack_modes=[AttackMode.DIRECT_FIRE],
        ),
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
        ),
    )

    air_robot = AirRobot(
        entity_id="air.uav.strike.01",
        sys_id="UAV_STRIKE_01",
        model="MK4V2-10",
        status=EntityOperationalState.READY,
        machine_type=MachineType.ROBOT,
        payload=payload_common,
        effects=AirEffectsSchema(
            has_launchers=False,
            payload_mounts=payload_common.payload_mounts,
            effect_domain=EffectDomain.LAND,
            launch_domain=OperationalDomain.AIR,
            guidance=GuidanceType.FPV,
            warhead=WarheadType.HEAT,
            pylon_format="",
            reusable=False,
            attack_modes=[AirAttackMode.ONEWAY],
        ),
        navigation=AirNavigationSchema(
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
            autopilot_fw=FirmwareInfo(name="INAV", version="8.0"),
        ),
        remote_control=RemoteControlSchema(
            links={"RC": rc_link, "VIDEO": video_link},
            rc_link="ELRS_915",
            vid_link="FPV_VIDEO",
            ctrl_video_sep=True,
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
        link_loadout=[
            ItemCount(item_type="ELRS_915", qty=3),
            ItemCount(item_type="FPV_VIDEO", qty=2),
        ],
        tac_e_comp=[
            ItemCount(item_type="robot.ugv.01", qty=1),
            ItemCount(item_type="air.uav.strike.01", qty=2),
        ],
        personnel=[ItemCount(item_type="personnel", qty=6)],
        vehicles=[ItemCount(item_type="pickup", qty=1)],
        air_units=[ItemCount(item_type="air.uav.strike.01", qty=2)],
        spacing=500.0,
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
        f"unpacked_msgpack_ground_robots={[robot.entity_id for robot in roundtrip['unpacked_msgpack_ground_robots']]}"
    )
    print(
        f"unpacked_msgpack_air_robots={[machine.entity_id for machine in roundtrip['unpacked_msgpack_air_robots']]}"
    )
    print(
        f"unpacked_msgpack_ground_orgs={[org.org_uid for org in roundtrip['unpacked_msgpack_ground_orgs']]}"
    )


if __name__ == "__main__":
    main()
