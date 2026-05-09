#### Robot

[variants] by PhysicalDomain:
- AIR: AirRobot (UAV/UAS)
- LAND: LandRobot (UGV)
- SEA: SeaRobot (USV)
- SUBSEA: SubseaRobot (UUV)
- SPACE: SpaceRobot

[facets]:
- domain (PhysicalDomain)
- autonomy ceiling (AutonomyClass) — ceiling capability, not current mode

AirRobot [facets]:
- airframe config (MultirotorConfig, FixedWingConfig, VTOLConfig as applicable)
- launch method
- recovery method
- propulsion (PropulsionType)
- max range, max flight time, max speed, cruise speed, max altitude
- weather limits

LandRobot [facets]:
- propulsion (LandPropulsion)
- max range, max speed

