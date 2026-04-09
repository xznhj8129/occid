# Reference

## Frame

[enum] Local2D:
- LU
- LD
- RU
- RD

[enum] Local3D:
- FRD
- FLU
- NED
- ENU

[enum] GlobalFrame:
- WGS84
- ETRS89
- ECEF
- ECI
- TEME
- LVLH

[enum] AltitudeReference:
- AMSL
- HAE
- AGL
- Barometric
- StartRelative
- HAAT
- AboveSeaFloor
- BelowSeaSurface
- EGM96

[enum] BearingReference:
- TrueNorth
- MagneticNorth
- GridNorth
- RelativeToHeading

## Coordinate

[enum] CoordinateEncoding:
- Cartesian2D
- Cartesian3D
- LatLon
- UTM
- MGRS
- PlusCode
- ECI
- ENU
- Spherical

## Geometry

[enum] GeometryType:
- Point
- Line
- Path
- Polygon
- Volume
- Orientation
- Arc
- Ellipse
- Ellipsoid
- Frustum
- Corridor
- Annulus

## Time

[facets] Timestamp:
- value (epoch, integer)

[facets] TimeWindow:
- start time, end time

[facets] Duration:
- value (seconds or milliseconds)

[facets] PhaseTime:
- h-hour reference, offset

[enum] TimeSyncSource:
- GPS
- NTP
- PTP
- Manual
- RadioTimeSignal

Staleness [facets]:
- age in seconds
- stale threshold

## Type

[enum] PhysicalDomain:
- Land
- Air
- Sea
- Undersea
- Space

[enum] Environment:
- Unknown
- Air
- Surface
- SubSurface
- Land
- Space

[enum] CombatDomain:
- Combat
- CombatSupport
- CombatSupportService

[enum] OpDomain:
- Land
- Air
- Sea
- Undersea
- Space
- Radio
- Psychological
- Cyber

[enum] Faction:
- UNKNOWN
- PENDING
- FRIENDLY
- SUSPECT
- HOSTILE
- NEUTRAL
- ASSUMED
- FAKER
- JOKER

[enum] Disposition:
- Unknown
- Friendly
- Hostile
- Suspicious
- AssumedFriendly
- Neutral
- Pending

[enum] ClassificationLevel:
- Unclassified
- ControlledUnclassified
- Confidential
- Secret
- TopSecret

[enum] ClassificationCaveat:
- NOFORN
- REL_TO
- FVEY
- NATO
- EU
- COSMIC
- ATOMAL

[enum] Nationality:
(100+ countries per Lattice — Albania through Zimbabwe, plus NATO, UN, InternationalRedCross)

[enum] MilitaryBranch:
- Army
- Navy
- AirForce
- Marines
- CoastGuard
- SpaceForce
- SpecialOperations
- Joint

[enum] EntityStatus:
- Active
- Inactive
- Unknown
- Offline
- Online
- Present
- Damaged
- Destroyed
- Lost
- Decoy

[enum] Priority:
- Routine
- Priority
- Immediate
- Flash
- FlashOverride
- CRITIC

[enum] PACE:
- Primary
- Alternate
- Contingency
- Emergency

[enum] ThreatLevel:
- Green
- Amber
- Red
- Black

[enum] DDILCondition:
- Normal
- Limited
- Intermittent
- Disrupted
- Denied

[enum] InteropLevel:
- Level1_IndirectRelay
- Level2_DirectReceipt
- Level3_PayloadControl
- Level4_FlightControl
- Level5_LaunchRecovery

[enum] UnitFunction:
- Maneuver
- FireSupport
- AirDefense
- Aviation
- Engineer
- Signal
- MilitaryIntelligence
- MilitaryPolice
- CBRN
- Logistics
- Medical
- CivilAffairs
- PsyOps
- SOF

[enum] WarfareType:
- Conventional
- Unconventional
- Guerrilla
- Hybrid
- Asymmetric
- Information
- Cyber
- Electronic

## Structs

Reusable data shapes built on Reference primitives.
Ontologically part of Reference, not a separate root.

### Primitives

Vector2D [facets]:
- two-axis float vector (x, y)

Vector3D [facets]:
- three-axis float vector (x, y, z)

Quaternion [facets]:
- rotation quaternion (x, y, z, w)

EulerAngles [facets]:
- yaw, pitch, roll

### Measurement

Measurement [facets]:
- value (float)
- sigma / uncertainty (float, optional)

### Bearing

Bearing [facets]:
- value (degrees 0-360)
- reference (BearingReference)

Heading [facets]:
- value (degrees 0-360)
- reference (BearingReference)

Course [facets]:
- value (degrees 0-360)
- reference (BearingReference)

### Geographic Positions

Position structs carry their own coordinate encoding and frame
as const metadata, so the consumer always knows how to interpret them.

LatLon [facets]:
- coordinate encoding (const, LatLon)
- reference frame (GlobalFrame)
- geometry type (const, Point)
- latitude
- longitude

LLA [facets]:
- latitude, longitude
- altitude with reference (AltitudeReference)
- optional: altitude_hae, altitude_agl, altitude_asf, pressure_depth

MGRS [facets]:
- coordinate encoding (const, MGRS)
- reference frame (GlobalFrame)
- geometry type (const, Point)
- grid zone, band, easting, northing

UTM [facets]:
- coordinate encoding (const, UTM)
- reference frame (GlobalFrame)
- geometry type (const, Point)
- zone, band, easting, northing

PlusCode [facets]:
- code string

ECI [facets]:
- x, y, z (doubles)

ENU [facets]:
- e, n, u (doubles) — used for velocity, acceleration

Spherical [facets]:
- azimuth, elevation, range

AzimuthElevation [facets]:
- azimuth
- elevation
- reference (BearingReference)

MagneticDeclination [facets]:
- declination value
- validity date
- location reference

### Local Positions

LocalPosition [facets]:
- inherits Vector2D

### Lines

Line2D [facets]:
- start point (Vector2D), stop point (Vector2D)

Line3D [facets]:
- start point (Vector3D), stop point (Vector3D)

### Paths

Path2D [facets]:
- ordered list of Vector2D

Path3D [facets]:
- ordered list of Vector3D

LLAPath [facets]:
- ordered list of LLA
- loop (bool)

### Polygons and Shapes

Polygon [facets]:
- ordered list of LLA (closed ring)

GeoEllipse [facets]:
- semi-major axis, semi-minor axis, orientation, height

GeoEllipsoid [facets]:
- forward axis, side axis, up axis

Arc [facets]:
- center
- radius
- start angle
- end angle

Annulus [facets]:
- center
- inner radius
- outer radius

Frustum [facets]:
- apex
- direction (AzimuthElevation)
- horizontal field of view
- vertical field of view
- near range
- far range

Sector [facets]:
- center
- radius
- start bearing
- end bearing

OrbitGeometry [facets]:
- center
- radius
- altitude
- direction
- speed

RacetrackGeometry [facets]:
- point A
- point B
- width
- altitude
- direction

CorridorGeometry [facets]:
- centerline
- width
- floor altitude
- ceiling altitude

### Bounding Boxes

Box2D [facets]:
- four corners (Vector2D)

Box3D [facets]:
- four corners (Vector3D)

### Error / Uncertainty

ErrorEllipse [facets]:
- probability
- semi-major axis, semi-minor axis, orientation

CovarianceMatrix3x3 [facets]:
- symmetric upper triangle (mxx, mxy, mxz, myy, myz, mzz)

[enum] AccuracyMethod:
- Calculated
- Estimated
- Measured
- Surveyed
- Unknown

CEP [facets]:
- radius
- probability basis

LEP [facets]:
- linear error
- probability basis

SEP [facets]:
- spherical error
- probability basis

DRMS [facets]:
- distance root mean square

PositionAccuracy [facets]:
- horizontal accuracy
- vertical accuracy
- accuracy method (AccuracyMethod)

### Pose

Pose [facets]:
- position (LLA)
- attitude (Quaternion) — body-to-ENU transform

### Range

FloatRange [facets]:
- lower bound, upper bound

UInt32Range [facets]:
- lower bound, upper bound

DoubleRange [facets]:
- min, max

DurationRange [facets]:
- min, max (Duration)

### Transforms

RigidTransform [facets]:
- rotation (Quaternion)
- translation (Vector3D)

TransformMatrix [facets]:
- 2x2 matrix (TMat2)
- 3x3 matrix (TMat3)
- 4x4 matrix (TMat4f)

### Compact Encodings

CompactPosition [facets]:
- lat (int32 degE7), lon (int32 degE7), alt (int32 cm)

### Orbital Mechanics

OrbitMeanElements [facets]:
- metadata (epoch, theory)
- mean elements (MeanKeplerianElements)
- TLE parameters (optional)

OrbitMeanElementsMetadata [facets]:
- epoch
- mean element theory (MeanElementTheory)

MeanKeplerianElements [facets]:
- semi-major axis
- eccentricity
- inclination
- right ascension
- argument of perigee
- mean anomaly
- mean motion
- eccentric anomaly

TleParameters [facets]:
- line 1 data
- line 2 data
- epoch
- mean motion derivative
- drag term

[enum] MeanElementTheory:
- SGP4

[enum] EciReferenceFrame:
- TEME

### Additional Coordinate / Geometry Shapes

ThetaPhi [facets]:
- theta (azimuth angle)
- phi (elevation angle)

AERPolygon [facets]:
- ordered list of azimuth-elevation-range points

LLAPolygon [facets]:
- ordered list of LLA points (closed ring)

LLAPath [facets]:
- ordered list of LLA
- loop (bool)

### Vector Variants

Vec2 [facets]:
- x, y (float)

Vec2f [facets]:
- x, y (float, explicit)

Vec3 [facets]:
- x, y, z (float)

Vec3f [facets]:
- x, y, z (float, explicit)

YawPitch [facets]:
- yaw, pitch

YPR [facets]:
- yaw, pitch, roll

### Color

Color [facets]:
- red, green, blue, alpha

[enum] MilColor:
- Red
- Blue
- Green
- Yellow
- Orange
- Purple
- White
- Black
- Brown
- Pink

### Units

[enum] DistanceUnit:
- Meters
- Kilometers
- Feet
- Yards
- NauticalMiles
- StatuteMiles

[enum] SpeedUnit:
- MetersPerSecond
- Knots
- KilometersPerHour
- MilesPerHour

[enum] TemperatureUnit:
- Celsius
- Fahrenheit
- Kelvin

[enum] PressureUnit:
- Hectopascal
- Millibar
- InchesOfMercury

[enum] AngleUnit:
- Degrees
- Radians
- Mils_NATO
- Mils_Warsaw
- Gradians

[enum] MassUnit:
- Kilograms
- Pounds
- Tons_Metric
- Tons_Short

[enum] UnitOfMeasure:
- Each
- Kilogram
- Liter
- Round
- Box
- Case
- Pallet
- Meter
- SquareMeter
- CubicMeter
- Hour

[enum] VolumeUnit:
- Liters
- Gallons_US
- Gallons_Imperial
- CubicMeters

[enum] ForceUnit:
- Newtons
- PoundsForce

[enum] PowerUnit:
- Watts
- Kilowatts
- Horsepower

[enum] FrequencyUnit:
- Hertz
- Kilohertz
- Megahertz
- Gigahertz

[enum] DataRateUnit:
- BitsPerSecond
- KilobitsPerSecond
- MegabitsPerSecond
- GigabitsPerSecond

Color [facets]:
- red
- green
- blue
- alpha

[enum] MilColor:
- Red
- Blue
- Green
- Yellow
- Orange
- Purple
- White
- Black
- Brown
- Pink

[enum] MarkerColor:
- Red
- Green
- Yellow
- White
- IR
- Orange
- Violet
- Blue

