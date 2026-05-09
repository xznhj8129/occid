### State
Telemetric, changing data about the condition of an object at a given time.

#### Kinematic

Kinematic [facets]:
- attitude (rotation, eg Quaternion or EulerAngles)
- ground speed
- airspeed (optional)
- velocity vector (optional, ENU)
- acceleration vector (optional, ENU)
- angular rate vector (optional)
- heading
- course
- climb rate
- throttle

#### Location

Location [facets]:
- position (geographic, eg LLA)
- altitude (meters, with reference datum)
- satellite count (optional, GPS quality indicator)
- velocity ENU (optional)
- speed (scalar, optional)
- acceleration ENU (optional)
- attitude (Quaternion, body→ENU, optional)

IndoorPosition [facets]:
- building reference
- floor number
- room identifier
- x offset
- y offset
- location method (IndoorPosMethod)

DeadReckoningState [facets]:
- last fix position
- last fix time
- estimated position
- drift estimate
- method

RelativePosition [facets]:
- reference entity
- offset
- frame

LocationUncertainty [facets]:
- position covariance (CovarianceMatrix3x3, ENU)
- velocity covariance (CovarianceMatrix3x3, ENU)
- error ellipse (ErrorEllipse)
- circular error (CE)
- linear error (LE)

#### Navigation

Navigation [facets]:
- navigation mode
- fix type
- global position valid
- home position valid
- position source
- heading source
- altitude source
- GNSS diagnostic statistics

NavigationState [facets]:
- navigation mode
- fix type
- position source
- heading source
- altitude source
- raw GNSS sample
- GNSS diagnostics

RawGNSSSample [facets]:
- latitude
- longitude
- absolute altitude
- ground speed
- ground course
- HDOP
- VDOP
- yaw

GNSSDiagnostics [facets]:
- last message age
- error count
- timeout count
- HDOP
- EPH
- EPV

#### Sensor

[variants] by kind:
- IMU: IMUState
- READINESS: SensorReadiness

IMUState [facets]:
- acceleration vector
- angular rate vector
- magnetic field vector
- temperature (optional)
- timestamp (optional)
- frame (optional)

SensorReadiness [facets]:
- gyro ready
- accel ready
- mag ready
- local position ready
- global position ready
- home position ready
- armable

FieldOfView [facets]:
- horizontal field of view
- vertical field of view
- minimum range
- maximum range

ProjectedFrustum [facets]:
- apex position
- direction (AzimuthElevation)
- horizontal field of view
- vertical field of view
- near range
- far range

RFConfiguration [facets]:
- center frequency
- bandwidth range
- operational modes

Bandwidth [facets]:
- center frequency
- bandwidth

BandwidthRange [facets]:
- min frequency
- max frequency

#### Input

Input [facets]:
- RC channel values
- receiver calibration / min / max / center
- channel mapping
- mode ranges

RCInputState [facets]:
- RC channel values

ReceiverConfig [facets]:
- min pulse
- max pulse
- center pulse

ChannelMap [facets]:
- channel mapping entries

ModeRangeSet [facets]:
- mode ranges

#### Resources

[variants] by resource type:
- BATTERY: Battery
- FUEL: Fuel
- CONSUMABLE: Consumable

Battery [facets]:
- voltage
- current draw (optional)
- remaining percentage
- remaining capacity
- temperature (optional)
- cell voltages (optional list)
- cell count (optional)
- power watts
- consumed charge / energy
- source identifier (optional)
- link quality proxy / RSSI (optional)

Fuel [facets]:
- volume (or gallons)
- remaining percentage
- max capacity
- operational requirement
- consumption rate

Consumable [facets]:
- total count
- remaining count

PowerSource [facets]:
- status (PowerStatus)
- type (PowerType)
- level (PowerLevel: capacity, remaining, percent, voltage, current, run time, consumption rate)
- offloadable (bool)

#### Condition

Condition [facets]:
- readiness level
- fault list
- damage assessment

Health [facets]:
- overall health status (HealthStatus)
- connection status (ConnectionStatus)
- component health map (ComponentHealth by ID)
- alerts (list of Alert)

ComponentHealth [facets]:
- component identifier
- health status (HealthStatus)
- last update time
- error codes (optional list)

ComponentMessage [facets]:
- component identifier
- message text
- severity (AlertLevel)
- timestamp

Alert [facets]:
- alert level (AlertLevel)
- condition (AlertCondition)
- message
- timestamp

AlertCondition [facets]:
- condition identifier
- description
- severity (AlertLevel)
- acknowledged flag
- timestamp

#### Lifecycle

#### Internal

Internal [facets]:
- operational mode
- error codes
- cpu load, memory used, disk used
- uptime
- temperature
- software version, build hash
- FC connectivity
- cycle time
- flight controller identity

SoftwareState [facets]:
- version
- build hash
- last updated
- config hash

AutopilotState [facets]:
- mode
- armed state
- in-air state
- throttle percentage
- navigation mode
- geofence active
- failsafe active

FlightControllerIdentity [facets]:
- API version
- FC variant
- board info
- hardware UID
- legacy UID
- vendor ID
- vendor name
- product ID
- product name
- flight software version
- flight software git hash
- OS software version
- OS software git hash

#### Mission

MissionProgress [facets]:
- current waypoint index
- total waypoints
- mission valid

WaypointStatus [facets]:
- total waypoint count
- current waypoint index
- mission valid

