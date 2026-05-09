#### Platform

[variants] by function:
- LAUNCHER: Launcher
- CHARGER: Charger
- RELAY: Relay
- RELAY_STATION: RelayStation
- CHARGING_STATION: ChargingStation
- LAUNCH_PAD: LaunchPad
- RECOVERY_SYSTEM: RecoverySystem
- GCS: GroundControlStation
- COMMAND_POST: MobileCommandPost
- SENSOR_PLATFORM: SensorPlatform
- OPERATOR_STATION: OperatorStation

GroundControlStation [facets]:
- operator station count
- supported protocols
- mobile (bool)

MobileCommandPost [facets]:
- vehicle reference
- communications suite
- battle management system

RelayStation [facets]:
- coverage area
- supported carriers
- gain / amplification

ChargingStation [facets]:
- connector types
- max simultaneous clients
- power output

LaunchPad [facets]:
- supported launch methods
- max vehicle weight
- orientation

RecoverySystem [facets]:
- recovery method
- max vehicle weight
- cycle time

