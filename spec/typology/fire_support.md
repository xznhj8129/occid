# Fire Support [Control → Directive + Communication → Command]

[enum] EngagementMethod:
- PointTarget
- AreaTarget
- Suppression
- Destruction
- Neutralization
- Illumination
- Smoke
- Marking

[enum] FireType:
- Immediate
- Planned
- OnCall

[enum] WeaponType:
- Mortar
- Howitzer
- Rocket
- MLRS
- Missile
- DirectFire
- AirDelivered
- Naval

[enum] AmmunitionType:
- HE
- WP
- Illumination
- Smoke
- DPICM
- Thermobaric
- HEAT
- Frag
- AP
- Incendiary
- Guided

[enum] ShellTrajectory:
- Low
- High
- Vertical

[enum] FireMissionStatus:
- Requested
- Approved
- Denied
- ShotOut
- SplashOver
- RoundsComplete
- EndOfMission
- Cancelled
- CheckFiring

[enum] EffectAchieved:
- Destroyed
- Neutralized
- Suppressed
- NoEffect
- Unknown

CallForFire [facets]:
- target reference or position
- engagement method
- requested munition
- fire type
- observer

FireMission [facets]:
- target reference
- engagement method
- weapon type
- ammunition type
- mission status

