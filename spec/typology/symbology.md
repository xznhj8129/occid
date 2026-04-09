# Symbology [Data → Properties]

MilStd2525C [facets]:
- SIDC (symbol identification coding string)

[enum] Severity:
- Info
- Low
- Medium
- High
- Critical
- Emergency

[enum] GeofenceResponse:
- None
- Report
- Warn
- Loiter
- RTL
- Land
- Brake
- MissionPause
- Fence

[enum] FailsafeType:
- RCLost
- DataLinkLost
- BatteryLow
- BatteryCritical
- GPSLost
- GeofenceBreach
- MotorFailure
- IMUFailure
- BarometerFailure
- TerrainFollowLost
- MissionInvalid
- CommunicationLost
- HighWind
- Crash

GimbalState [facets]:
- current azimuth
- current elevation
- current horizontal field of view
- current vertical field of view
- stabilized
- mode
- tracking entity reference

CameraState [facets]:
- recording
- photos taken
- storage remaining percentage
- current zoom
- current field of view
- resolution
- frame rate

SequenceGap [facets]:
- source reference
- expected sequence
- received sequence
- gap count
- detection time

CompressionPolicy [facets]:
- algorithm
- compression level
- minimum message size

CompactTelemetry [facets]:
- short entity identifier
- compact position
- heading
- speed
- battery percentage
- status flags

