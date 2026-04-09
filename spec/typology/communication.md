# Communication

## Node
Endpoint that transmits or receives.
An Entity can have multiple Nodes. Each Node has its own Transport(s).
Binding: Entity → Node → Transport.

[facets]:
- entity reference (what Entity this node belongs to)
- node capabilities

[enum] NodeType:
- Sensor
- Effector
- C2
- Relay
- Gateway
- Observer
- All

NodeCapabilities [facets]:
- can transmit
- can receive
- can relay
- can process

NetworkInterface [facets]:
- node reference
- carrier reference
- address
- port
- state

## Transport

### Network

[enum] NetworkTopology:
- Mesh
- PointToPoint
- Broadcast
- StoreAndForward

[enum] MeshNodeRole:
- Router
- Endpoint
- Repeater
- Gateway
- BorderRouter

[enum] MeshRoutingProtocol:
- AODV
- OLSR
- Babel
- Batman
- Custom

### Carrier

[variants] by medium:
- RADIO: RadioCarrier
- WIRE: WireCarrier
- IP: IPCarrier
- SATELLITE: SatelliteCarrier
- CELLULAR: CellularCarrier
- VOICE: VoiceCarrier — terminal, analog, no protocol

RadioCarrier [facets]:
- band (EMBand)
- frequency
- channel
- bandwidth
- waveform
- crypto type, crypto keys

WireCarrier [facets]:
- baud rate

SatelliteCarrier [facets]:
- band (SATCOMBand)
- orbit type (LEO, MEO, GEO)
- terminal type

[enum] EMBand:
- ELF
- SLF
- ULF
- VLF
- LF
- MF
- HF
- VHF
- UHF
- SHF
- EHF
- THF
- Infrared
- Visible

[enum] SATCOMBand:
- UHF
- SHF
- EHF
- Ka
- Ku
- X
- C
- L
- S

[enum] DataLinkType:
- CDL
- TCDL
- SADL
- Link16
- Link22
- JREAP
- BACN
- BLOS
- DAMA
- HaveQuick
- SINCGARS
- ARC_210

### Protocol

[enum] ProtocolType:
- MAVLink
- MAVLink_M
- MSPv2
- ROS
- STANAG4586
- CoT — Cursor on Target
- CustomSerial
- Meshtastic
- RTP_RTSP — video streaming
- SRT
- HLS
- WebRTC
- Link16
- VMF
- ADS_B
- XMPP
- DDS

[facets]:
- version
- serialization form (SerializationFormat)

[enum] SerializationFormat:
- Protobuf
- JSON
- XML
- CBOR
- MessagePack
- FlatBuffers
- Avro
- BSON
- Binary_Custom
- ASCII_Text

[enum] CompressionType:
- None
- GZIP
- LZ4
- Zstd
- Snappy
- Deflate

[enum] Endianness:
- LittleEndian
- BigEndian
- NetworkOrder

[enum] QoSReliability:
- BestEffort
- AtLeastOnce
- ExactlyOnce
- Guaranteed

[enum] RoutingMode:
- Unicast
- Multicast
- Broadcast
- Anycast
- PubSub
- RequestReply
- StoreAndForward

QoS [facets]:
- max latency
- minimum bandwidth
- reliability (QoSReliability)
- priority

Topic [facets]:
- namespace
- name

Subscription [facets]:
- subscriber
- topic
- filter
- QoS

COMSEC [facets]:
- encryption algorithm
- key material reference
- key changeover schedule

TRANSEC [facets]:
- frequency hopping set
- hop rate
- synchronization method

## Feed

[variants] by data flow shape:
- LINK: Link — discontinuous discrete packets
- STREAM: Stream — continuous indeterminate-size flow

Stream [variants] by content:
- VIDEO: VideoStream
- AUDIO: AudioStream
- SENSOR: SensorStream

[enum] StreamEncoding:
- H264
- H265
- VP8
- VP9
- AV1
- MJPEG
- RAW
- PCM
- AAC
- Opus

[enum] StreamTransport:
- RTP
- RTSP
- SRT
- HLS
- WebRTC
- MPEG_TS
- NDI
- RTMP

VideoStream [facets]:
- encoding (StreamEncoding)
- transport (StreamTransport)
- resolution, frame rate, bitrate, latency

SensorStream [facets]:
- stream purpose
- encoding
- transport
- source entity

## Message

[enum] MessageShape:
- Snapshot — whole state at a point in time
- Delta — only changes at a point in time
- History — only changes over time
- Log — whole state over time

[enum] DataFlowType:
- CommandDown — intent-bearing, reliable, ACK'd, small, infrequent
- StatusUp — task-coupled reporting, reliable, ACK'd, infrequent
- TelemetryUp — entity-state broadcast, lossy-tolerant, fire-and-forget, frequent

[enum] MessagePriority:
- Routine
- Priority
- Immediate
- Flash
- FlashOverride

[enum] AcknowledgmentPolicy:
- None
- OnReceipt
- OnProcessing
- OnExecution

MessageClassification [facets]:
- classification level
- caveats
- releasability

MessageEnvelope [facets]:
- message identifier
- timestamp
- source node
- destination nodes
- priority
- classification
- TTL
- sequence number
- correlation identifier
- retry count
- acknowledgment policy

DeliveryReceipt [facets]:
- message identifier
- receiving node
- received time
- receipt status

TransmissionResult [facets]:
- target count
- bytes sent

TransponderCodes [facets]:
- mode 1, mode 2, mode 3 (squawk codes)
- mode 4 interrogation response
- mode 5 (response, code, platform ID)
- mode S (id string, ICAO address)

[enum] InterrogationResponse:
- Correct
- Incorrect
- NoResponse

[variants] by purpose:
- COMMAND: Command
- TELEMETRY: Telemetry
- OBSERVATION: Observation
- RESPONSE: Response

### Command
Directs or controls.

[variants] by target:
- FLIGHT: FlightCommand
- NAVIGATION: NavigationCommand
- MODE: ModeCommand
- PARAMETER: ParameterCommand
- ACTUATOR: ActuatorCommand
- FIRE_SUPPORT: FireSupportCommand — immediate fire control only (adjust, cease, check); call-for-fire initiates FireMissionTask
- EW_COMMAND: EWCommand — immediate start/stop only (cease jam, start emission); sustained operations are EWActionTask
- COMMS_COMMAND: CommunicationCommand
- EMERGENCY: EmergencyCommand
- GIMBAL: GimbalCommand
- CAMERA: CameraCommand

[enum] GimbalMode:
- Stow
- Manual
- TrackEntity
- PointAtPosition
- PointAtAzEl
- ScanPattern
- StabilizedHold
- ReturnToCenter

[enum] OODACycle:
- Observe
- Orient
- Decide
- Act

[enum] CameraAction:
- TakePhoto
- StartRecording
- StopRecording
- SetZoom
- SetFocus
- SetExposure
- SetWhiteBalance
- SetPalette
- ToggleNightVision

FlightCommand [variants] by action:
- ARM: ArmCommand
- DISARM: DisarmCommand
- TAKEOFF: TakeoffCommand
- LAND: LandCommand
- RTL: ReturnToLaunchCommand
- SET_TAKEOFF_ALTITUDE: SetTakeoffAltitudeCommand

SetTakeoffAltitudeCommand [facets]:
- target altitude

NavigationCommand [variants] by action:
- GO_TO: GoToCommand
- SET_WAYPOINT: SetWaypointCommand
- SELECT_MISSION: SelectMissionCommand

[enum] WaypointActionType:
- Transit
- Flyover
- Flyby
- Takeoff
- Land
- Loiter
- Orbit
- Hold
- ReturnToLaunch
- PayloadAction
- SensorAction
- Photo
- Survey
- Delivery
- Relay
- Rendezvous
- Custom

GoToCommand [facets]:
- destination position
- target altitude
- target yaw

SetWaypointCommand [facets]:
- sequence index
- waypoint action (WaypointActionType)
- destination position
- target altitude
- action parameters
- flags

SelectMissionCommand [facets]:
- mission sequence index

ModeCommand [variants] by action:
- SET_MODE: SetModeCommand

SetModeCommand [facets]:
- mode identifier
- enabled state

### Telemetry
Reports the sender's own internal state.
Composes State data by reference — does not flatten fields.

[variants] by scope:
- UAV: UAVTelemetry

UAVTelemetry [facets]:
- location (Location) — position, altitude, fix quality, satellite count, uncertainty, home/global validity
- navigation state (Navigation) — nav mode, source selection, fix source, validity, GNSS diagnostic statistics
- kinematic state (Kinematic) — attitude, angular rates, ground speed, ground course, airspeed, climb rate, heading, throttle
- sensor state (Sensor) — IMU sample, sensor readiness, calibration / availability state
- input state (Input) — RC channels, receiver config, channel map, mode ranges
- resource state (Battery, Fuel, Consumable as applicable) — battery / analog power telemetry, remaining, consumed, temperature
- parameters (Robot Parameters) — flight mode, armed, in-air, active modes, override active, failsafe state
- internal state (Internal) — FC connectivity, CPU load, cycle time, software / board / build identity
- condition (Condition) — sensor readiness, armable status, fault / warning indicators
- mission progress (MissionProgress) — current waypoint, total waypoints, mission validity

### Observation
Reports external objects, events, or environment.
Carries Intel data (Detection, Classification, Track).

CoTEvent [facets]:
- UID
- CoT type
- production method
- callsign
- event time
- start time
- stale time
- geographic position
- CE
- LE
- detail XML
- source host
- source port
- targets

MarkerMessage [facets]:
- UID
- callsign
- marker CoT type
- geographic position
- CE
- LE
- stale period
- targets

GeoChatMessage [facets]:
- UID
- message text
- sender callsign
- recipient team
- geographic position
- CE
- LE
- targets

ParseErrorMessage [facets]:
- error text

### Response

[variants] by nature:
- ACK: Ack
- NACK: Nack
- RESULT: Result

### CoT Reply Codes (mapping to Response variants)

[enum] ReplyCode:
- Received
- Wilco
- Complete_Success
- Complete_Fail
- Fail_NoAssets
- Fail_BadRequest
- Fail_Denied
- Fail_InsufficientInfo
- Fail_Rejected
- Fail_RejectedByC2
- Fail_RejectedByPlatform
- Fail_Stale
- Status_Canceling
- Status_Executing
- Status_Review

Heartbeat [facets]:
- node reference
- timestamp
- uptime
- status summary
- interval configuration

HeartbeatConfig [facets]:
- interval
- timeout
- jitter

[enum] ScheduleType:
- ZoneEnabled
- ZoneTempEnabled

Schedule [facets]:
- schedule type (ScheduleType)
- cron windows
- enabled state
- validity window

CronWindow [facets]:
- cron expression
- timezone
- active from
- active until

### CoT Production Method (how data was produced)

[enum] ProductionMethod:
- Machine_GPS
- Machine_INS
- Machine_INS_GPS
- Machine_DGPS
- Machine_Mensurated
- Machine_Magnetic
- Machine_Simulated
- Machine_Configured
- Machine_Passed
- Machine_Fused
- Machine_Tracker
- Machine_Radio
- Machine_Radio_EPLRS
- Machine_Radio_PLRS
- Machine_Radio_Doppler
- Machine_Radio_VHF
- Machine_Radio_TADIL_A
- Machine_Radio_TADIL_B
- Machine_Radio_TADIL_J
- Human_Transcribed
- Human_Estimated
- Human_Calculated
- Human_Pasted
- Human_GIGO

### CoT Relation Types

[enum] RelationType:
- Parent
- Producer
- Owner
- Manager
- Leader
- Child
- Correlated
- Fused
- Composite
- Alternate
- Refinement
- Amplification
- RefinementURL
- TaskingBy
- TaskObject
- TaskIndirectObject
- TaskSubject
- TaskAt
- TaskBy
- TaskWith
- TaskFrom
- TaskRegarding

### CoT Operational Context

[enum] OperationalContext:
- Exercise
- Operational
- Simulated

