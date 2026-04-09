#### Vehicle

[variants] by domain:
- LAND: LandVehicle
- AIR: AirVehicle
- SEA: SeaVehicle
- SUBSEA: SubseaVehicle
- SPACE: SpaceVehicle

[enum] LandVehicleClass:
- Light
- Armored

LandVehicle [facets]:
- class (LandVehicleClass)
- propulsion (LandPropulsion)

[enum] AirVehicleClass:
- Fighter
- Bomber
- Transport
- Tanker
- Trainer
- Reconnaissance
- Helicopter
- Tiltrotor
- LighterThanAir

AirVehicle [facets]:
- class (AirVehicleClass)
- propulsion (PropulsionType)

[enum] SeaVehicleClass:
- Frigate
- Destroyer
- Carrier
- Submarine
- Patrol
- Amphibious
- Auxiliary
- Merchant

SeaVehicle [facets]:
- class (SeaVehicleClass)

