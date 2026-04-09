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

[enum] AutonomyClass:
- Remote — directly piloted, no onboard autonomy
- Assisted — human controls, machine assists (stabilization, failsafes)
- SemiAutonomous — machine executes discrete tasks, human approves each
- Supervised — machine acts continuously, human monitors and can intervene
- Autonomous — machine acts independently within parameters

[enum] MultirotorConfig:
- Quad
- Hex
- Octo
- Coaxial
- Y6
- X8

[enum] FixedWingConfig:
- Conventional
- FlyingWing
- Canard
- TandemWing
- BlendedWingBody
- Delta

[enum] VTOLConfig:
- Tiltrotor
- Tailsitter
- LiftAndCruise
- QuadPlane
- CopterPlane

[enum] LaunchMethod:
- HTOL
- VTOL
- Catapult
- HandLaunch
- RailLaunch
- TubeLaunch
- DropLaunch
- BalloonLaunch

[enum] RecoveryMethod:
- HTOL
- VTOL
- Parachute
- DeepStall
- NetRecovery
- SkyHook
- BellyLand
- Ditching

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

