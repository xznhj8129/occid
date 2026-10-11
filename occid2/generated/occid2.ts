// GENERATED FILE - DO NOT EDIT
export type UID = Uint8Array; // Runtime representation: exactly 16 bytes.

export enum TaskPriority {
  ROUTINE = 0,
  HIGH = 1,
  IMMEDIATE = 2,
}

export enum TaskStatus {
  NEW = 0,
  ACTIVE = 1,
  COMPLETE = 2,
  FAILED = 3,
  CANCELLED = 4,
  ACCEPTED = 5,
}

export enum ControlLevel {
  NONE = 0,
  MONITOR = 1,
  GUIDE = 2,
  FULL = 3,
}

export enum PlanApprovalState {
  DRAFT = 0,
  PROPOSED = 1,
  APPROVED = 2,
  REJECTED = 3,
  SUPERSEDED = 4,
}

export enum BooleanOperator {
  NONE = 0,
  NOT = 1,
  AND = 2,
  OR = 3,
  XOR = 4,
  NAND = 5,
  NOR = 6,
  XNOR = 7,
}

export enum TaskIntent {
  MOVE = 0,
  HOLD = 1,
  LOCATE = 2,
  TRACK = 3,
  CREATE = 4,
  REMOVE = 5,
  MODIFY = 6,
  PROTECT = 7,
  IDENTIFY = 8,
  CLASSIFY = 9,
  FOLLOW = 10,
  MEASURE = 11,
  RESTORE = 12,
  DENY = 13,
  TRANSPORT = 14,
}

export enum CommandOperation {
  ENGAGE = 0,
  DISENGAGE = 1,
  PAUSE = 2,
  RESUME = 3,
  SET = 4,
  MOVE = 5,
  ALLOCATE = 6,
  TRANSFER = 7,
  LOAD_CONFIGURATION = 8,
  RESET = 9,
}

export const Substrate = {"BIOLOGICAL": "Substrate.BIOLOGICAL", "MECHANICAL": "Substrate.MECHANICAL", "CYBER": "Substrate.CYBER"} as const;
export const PhysicalDomain = {"LAND": "PhysicalDomain.LAND", "AIR": "PhysicalDomain.AIR", "SEA": "PhysicalDomain.SEA", "UNDERSEA": "PhysicalDomain.UNDERSEA", "SPACE": "PhysicalDomain.SPACE"} as const;
export const Controller = {"MANNED": "Controller.MANNED", "UNMANNED": "Controller.UNMANNED"} as const;
export const Locomotion = {"SELF_PROPELLED": "Locomotion.SELF_PROPELLED", "EXTERNAL": "Locomotion.EXTERNAL", "STATIC": "Locomotion.STATIC"} as const;
export const Airframe = {"MULTIROTOR": "Airframe.MULTIROTOR", "FIXED_WING": "Airframe.FIXED_WING"} as const;
export const Representation = {"Geodetic": "Representation.Geodetic", "LocalCartesian": "Representation.LocalCartesian", "LocalEuler": "Representation.LocalEuler", "Quaternion": "Representation.Quaternion"} as const;
export const BloodGroup = {"A_POS": "BloodGroup.A_POS", "A_NEG": "BloodGroup.A_NEG", "B_POS": "BloodGroup.B_POS", "B_NEG": "BloodGroup.B_NEG", "AB_POS": "BloodGroup.AB_POS", "AB_NEG": "BloodGroup.AB_NEG", "O_POS": "BloodGroup.O_POS", "O_NEG": "BloodGroup.O_NEG"} as const;
export const Realm = {"WORLD": "Realm.WORLD", "INFORMATION": "Realm.INFORMATION"} as const;
export const TemporalMode = {"ACHIEVE": "TemporalMode.ACHIEVE", "MAINTAIN": "TemporalMode.MAINTAIN"} as const;
export const TruthTarget = {"TRUE": "TruthTarget.TRUE", "FALSE": "TruthTarget.FALSE"} as const;
export const AirMission = ["Mission", "PhysicalDomain.AIR"] as const;
export const AirTask = ["Task", "PhysicalDomain.AIR"] as const;
export const UGV = ["Substrate.MECHANICAL", "Locomotion.SELF_PROPELLED", "UnmannedVehicle", "Controller.UNMANNED", "PhysicalDomain.LAND"] as const;
export const UAV = ["Substrate.MECHANICAL", "Locomotion.SELF_PROPELLED", "UnmannedVehicle", "Controller.UNMANNED", "PhysicalDomain.AIR"] as const;
export const Drone = ["Substrate.MECHANICAL", "Locomotion.SELF_PROPELLED", "UnmannedVehicle", "Controller.UNMANNED", "PhysicalDomain.AIR", "Airframe.MULTIROTOR"] as const;
export const Geodetic = ["Representation.Geodetic"] as const;
export const LocalCartesian = ["Representation.LocalCartesian"] as const;
export const LocalEuler = ["Representation.LocalEuler"] as const;
export const Quaternion = ["Representation.Quaternion"] as const;
export const POSITION_GOAL = {"description": "An actor's position is the destination.", "factors": ["Task", "Realm.WORLD"], "given": {"actor": ["Entity"], "destination": ["Position"]}, "sought": {}, "equations": [{"quantity": "Position", "of": "actor", "equals": "destination"}], "words": []} as const;
export const POSITION_QUERY = {"description": "An entity's position is the answer.", "factors": ["Task", "Realm.INFORMATION"], "given": {"target": ["Entity"]}, "sought": {"position": ["Position"]}, "equations": [{"quantity": "Position", "of": "target", "equals": "position"}], "words": []} as const;
export const EXISTENCE_GOAL = {"description": "An object's existence is asserted.", "factors": ["Task", "Realm.WORLD", "TemporalMode.ACHIEVE", "Existence"], "given": {"object": ["Object"]}, "sought": {}, "equations": [], "words": []} as const;
export const OBJECT_STATE_GOAL = {"description": "An object's state is asserted.", "factors": ["Task", "Realm.WORLD"], "given": {"object": ["Object"]}, "sought": {}, "equations": [], "words": []} as const;
export const ENGAGEMENT_COMMAND = {"description": "The target's engagement state is asserted.", "factors": ["Command"], "given": {"target": ["Object"]}, "sought": {}, "equations": [], "words": []} as const;
export const PROCESS_COMMAND = {"description": "A running process is asserted paused or released.", "factors": ["Command", "Paused"], "given": {"target": ["Object"], "process": ["Text"]}, "sought": {}, "equations": [], "words": []} as const;
export const MOVE = {"description": "An actor's position is the destination.", "factors": ["Task", "Realm.WORLD", "TemporalMode.ACHIEVE"], "given": {"actor": ["Entity"], "destination": ["Position"]}, "sought": {}, "equations": [{"quantity": "Position", "of": "actor", "equals": "destination"}], "words": ["TaskIntent.MOVE"]} as const;
export const HOLD = {"description": "An actor's position is the destination.", "factors": ["Task", "Realm.WORLD", "TemporalMode.MAINTAIN"], "given": {"actor": ["Entity"], "destination": ["Position"]}, "sought": {}, "equations": [{"quantity": "Position", "of": "actor", "equals": "destination"}], "words": ["TaskIntent.HOLD"]} as const;
export const LOCATE = {"description": "An entity's position is the answer.", "factors": ["Task", "Realm.INFORMATION", "TemporalMode.ACHIEVE"], "given": {"target": ["Entity"]}, "sought": {"position": ["Position"]}, "equations": [{"quantity": "Position", "of": "target", "equals": "position"}], "words": ["TaskIntent.LOCATE"]} as const;
export const TRACK = {"description": "An entity's position is the answer.", "factors": ["Task", "Realm.INFORMATION", "TemporalMode.MAINTAIN"], "given": {"target": ["Entity"]}, "sought": {"position": ["Position"]}, "equations": [{"quantity": "Position", "of": "target", "equals": "position"}], "words": ["TaskIntent.TRACK"]} as const;
export const CREATE = {"description": "An object's existence is asserted.", "factors": ["Task", "Realm.WORLD", "TemporalMode.ACHIEVE", "Existence", "TruthTarget.TRUE"], "given": {"object": ["Object"]}, "sought": {}, "equations": [], "words": ["TaskIntent.CREATE"]} as const;
export const REMOVE = {"description": "An object's existence is asserted.", "factors": ["Task", "Realm.WORLD", "TemporalMode.ACHIEVE", "Existence", "TruthTarget.FALSE"], "given": {"object": ["Object"]}, "sought": {}, "equations": [], "words": ["TaskIntent.REMOVE"]} as const;
export const MODIFY = {"description": "An object's state is asserted.", "factors": ["Task", "Realm.WORLD", "TemporalMode.ACHIEVE"], "given": {"object": ["Object"]}, "sought": {}, "equations": [], "words": ["TaskIntent.MODIFY"]} as const;
export const PROTECT = {"description": "An object's state is asserted.", "factors": ["Task", "Realm.WORLD", "TemporalMode.MAINTAIN"], "given": {"object": ["Object"]}, "sought": {}, "equations": [], "words": ["TaskIntent.PROTECT"]} as const;
export const ENGAGE = {"description": "The target's engagement state is asserted.", "factors": ["Command", "TruthTarget.TRUE"], "given": {"target": ["Object"]}, "sought": {}, "equations": [], "words": ["CommandOperation.ENGAGE"]} as const;
export const DISENGAGE = {"description": "The target's engagement state is asserted.", "factors": ["Command", "TruthTarget.FALSE"], "given": {"target": ["Object"]}, "sought": {}, "equations": [], "words": ["CommandOperation.DISENGAGE"]} as const;
export const PAUSE = {"description": "A running process is asserted paused or released.", "factors": ["Command", "Paused", "TruthTarget.TRUE"], "given": {"target": ["Object"], "process": ["Text"]}, "sought": {}, "equations": [], "words": ["CommandOperation.PAUSE"]} as const;
export const RESUME = {"description": "A running process is asserted paused or released.", "factors": ["Command", "Paused", "TruthTarget.FALSE"], "given": {"target": ["Object"], "process": ["Text"]}, "sought": {}, "equations": [], "words": ["CommandOperation.RESUME"]} as const;
export const IDENTIFY = {"description": "Solve for the identity of an entity.", "factors": ["Task", "Realm.INFORMATION", "TemporalMode.ACHIEVE"], "given": {"target": ["Entity"]}, "sought": {"identity": ["Identity"]}, "equations": [{"quantity": "Identity", "of": "target", "equals": "identity"}], "words": ["TaskIntent.IDENTIFY"]} as const;
export const CLASSIFY = {"description": "Solve for the classification of an entity.", "factors": ["Task", "Realm.INFORMATION", "TemporalMode.ACHIEVE"], "given": {"target": ["Entity"]}, "sought": {"classification": ["Classification"]}, "equations": [{"quantity": "Classification", "of": "target", "equals": "classification"}], "words": ["TaskIntent.CLASSIFY"]} as const;
export const FOLLOW = {"description": "Follow a path.", "factors": ["Task", "Realm.WORLD", "TemporalMode.MAINTAIN"], "given": {"actor": ["Entity"], "path": ["GeoPath"]}, "sought": {}, "equations": [], "words": ["TaskIntent.FOLLOW"]} as const;
export const MEASURE = {"description": "Measure a state of a target.", "factors": ["Task", "Realm.INFORMATION", "TemporalMode.ACHIEVE"], "given": {"target": ["Entity"]}, "sought": {"measurement": ["State"]}, "equations": [], "words": ["TaskIntent.MEASURE"]} as const;
export const RESTORE = {"description": "Return an object to a prior state.", "factors": ["Task", "Realm.WORLD", "TemporalMode.ACHIEVE"], "given": {"object": ["Object"]}, "sought": {}, "equations": [], "words": ["TaskIntent.RESTORE"]} as const;
export const DENY = {"description": "Prevent connectivity to an object.", "factors": ["Task", "Realm.WORLD", "TemporalMode.MAINTAIN", "Connectivity", "TruthTarget.FALSE"], "given": {"object": ["Object"]}, "sought": {}, "equations": [], "words": ["TaskIntent.DENY"]} as const;
export const TRANSPORT = {"description": "Move a thing between places; which end and what moves are bindings.", "factors": ["Task", "Realm.WORLD", "TemporalMode.ACHIEVE"], "given": {"cargo": ["Object"], "origin": ["Position"], "destination": ["Position"]}, "sought": {}, "equations": [], "words": ["TaskIntent.TRANSPORT"]} as const;
export const SET = {"description": "Set a declared state property on the target.", "factors": ["Command"], "given": {"target": ["Object"], "property": ["Text"], "value": ["Scalar"]}, "sought": {}, "equations": [], "words": ["CommandOperation.SET"]} as const;
export const DIRECT = {"description": "Direct the target to a destination or along a path.", "factors": ["Command", "TemporalMode.ACHIEVE"], "given": {"target": ["Object"], "destination": ["Position"], "path": ["GeoPath"], "radius": ["Distance"], "speed": ["Speed"], "yaw": ["Angle"]}, "sought": {}, "equations": [{"quantity": "Position", "of": "target", "equals": "destination"}], "words": ["CommandOperation.MOVE"]} as const;
export const ALLOCATE = {"description": "Allocate a referenced resource.", "factors": ["Command"], "given": {"target": ["Object"], "resource": ["Resource"], "quantity": ["Count"]}, "sought": {}, "equations": [], "words": ["CommandOperation.ALLOCATE"]} as const;
export const TRANSFER = {"description": "Transfer a referenced resource.", "factors": ["Command"], "given": {"target": ["Object"], "resource": ["Resource"], "quantity": ["Count"]}, "sought": {}, "equations": [], "words": ["CommandOperation.TRANSFER"]} as const;
export const LOAD_CONFIGURATION = {"description": "Load a referenced configuration on the target.", "factors": ["Command"], "given": {"target": ["Object"], "parameter": ["Text"], "value": ["Scalar"]}, "sought": {}, "equations": [], "words": ["CommandOperation.LOAD_CONFIGURATION"]} as const;
export const RESET = {"description": "Reset the target to its initial state.", "factors": ["Command"], "given": {"target": ["Object"]}, "sought": {}, "equations": [], "words": ["CommandOperation.RESET"]} as const;

export interface Root {
}

export interface Object {
}

export interface Locality {
  name?: string | null;
}

export interface Entity {
  uid: UID;
  name?: string | null;
}

export interface Biological {
  uid: UID;
  name?: string | null;
}

export interface Person {
  uid: UID;
  name?: string | null;
}

export interface Actor {
  uid: UID;
  name?: string | null;
  role?: Role | null;
}

export interface Machine {
  uid: UID;
  name?: string | null;
  serial_number?: string | null;
}

export interface Vehicle {
  uid: UID;
  name?: string | null;
  serial_number?: string | null;
  model?: string | null;
}

export interface CrewedVehicle {
  uid: UID;
  name?: string | null;
  serial_number?: string | null;
  model?: string | null;
}

export interface UnmannedVehicle {
  uid: UID;
  name?: string | null;
  serial_number?: string | null;
  model?: string | null;
}

export interface Data {
}

export interface State {
}

export interface Position {
}

export interface Velocity {
}

export interface Attitude {
}

export interface Identity {
}

export interface Classification {
}

export interface Existence {
}

export interface Connectivity {
}

export interface Engagement {
}

export interface Activity {
}

export interface Paused {
}

export interface Hold {
}

export interface Text {
}

export interface Duration {
}

export interface Angle {
}

export interface Distance {
}

export interface Speed {
}

export interface Count {
}

export interface Ordinal {
}

export interface Code {
}

export interface Scalar {
}

export interface Altitude {
}

export interface GlobalPosition {
  lat: number;
  lon: number;
  h: number;
}

export interface LocalPosition {
  x: number;
  y: number;
  z: number;
}

export interface LocalVelocity {
  vx: number;
  vy: number;
  vz: number;
}

export interface LocalAttitude {
  roll: number;
  pitch: number;
  yaw: number;
}

export interface QuaternionAttitude {
  qw: number;
  qx: number;
  qy: number;
  qz: number;
}

export interface Mark {
  uid: UID;
  name?: string | null;
  lat: number;
  lon: number;
  h: number;
}

export interface Control {
}

export interface Directive {
}

export interface Task {
  uid: UID;
  instruction: string;
  intent: TaskIntent;
  priority?: TaskPriority;
  status?: TaskStatus;
}

export interface Mission {
}

export interface Time {
}

export interface Range {
}

export interface NumericRange {
  min_value?: number | null;
  max_value?: number | null;
}

export interface Condition {
}

export interface Predicate {
  subject_uid?: UID | null;
  quantity?: string | null;
  value?: number | null;
}

export interface BooleanLogic {
  operator: BooleanOperator;
  terms?: Array<Condition>;
}

export interface GeoPath {
  points?: Array<GlobalPosition>;
}

export interface Role {
  name?: string | null;
}

export interface Resource {
  uid?: UID | null;
  name?: string | null;
}

export interface Constraint {
  condition?: Condition | null;
}

export interface TaskTimeWindow {
  condition?: Condition | null;
  earliest_start?: number | null;
  latest_finish?: number | null;
}

export interface WeatherLimits {
  condition?: Condition | null;
  ifr?: boolean | null;
  night?: boolean | null;
  rain?: NumericRange | null;
  snow?: NumericRange | null;
  temp?: NumericRange | null;
  wind?: NumericRange | null;
  vis?: NumericRange | null;
  icing?: boolean | null;
}

export interface Objective {
  uid: UID;
  name: string;
  condition?: Condition | null;
  criteria?: Array<Condition>;
  priority?: TaskPriority;
  status?: TaskStatus;
  start_time?: number | null;
  deadline?: number | null;
}

export interface Command {
  uid: UID;
  operation: CommandOperation;
}

export interface Authority {
  uid: UID;
  role?: Role | null;
}

export interface Lease {
  uid: UID;
  role?: Role | null;
  bound?: Condition | null;
  control_level?: ControlLevel | null;
}

export interface Plan {
  uid: UID;
  name?: string | null;
  approval_state?: PlanApprovalState;
}

export interface PlanContingency {
  condition: Condition;
}

export const Directed = {"signature": ["Root", "Root"], "operand_names": ["source", "target"], "specializes": null} as const;
export const AssignedWork = {"signature": ["Entity", "Task"], "operand_names": ["assignee", "work"], "specializes": "Directed"} as const;
export const ConstrainedBy = {"signature": ["Control", "Constraint"], "operand_names": ["subject", "constraint"], "specializes": "Directed"} as const;
export const OwnedBy = {"signature": ["Objective", "Entity"], "operand_names": ["objective", "owner"], "specializes": "Directed"} as const;
export const Holds = {"signature": ["Authority", "Entity"], "operand_names": ["authority", "holder"], "specializes": "Directed"} as const;
export const GrantedBy = {"signature": ["Authority", "Entity"], "operand_names": ["authority", "grantor"], "specializes": "Directed"} as const;
export const Controls = {"signature": ["Lease", "Object"], "operand_names": ["lease", "asset"], "specializes": "Directed"} as const;
export const Contains = {"signature": ["Plan", "Root"], "operand_names": ["plan", "item"], "specializes": "Directed"} as const;
export const MODEL_IDS = {"Activity": 1, "Actor": 2, "Altitude": 3, "Angle": 4, "Attitude": 5, "Authority": 6, "Biological": 7, "BooleanLogic": 8, "Classification": 9, "Code": 10, "Command": 11, "Condition": 12, "Connectivity": 13, "Constraint": 14, "Control": 15, "Count": 16, "CrewedVehicle": 17, "Data": 18, "Directive": 19, "Distance": 20, "Duration": 21, "Engagement": 22, "Entity": 23, "Existence": 24, "GeoPath": 25, "GlobalPosition": 26, "Hold": 27, "Identity": 28, "Lease": 29, "LocalAttitude": 30, "LocalPosition": 31, "LocalVelocity": 32, "Locality": 33, "Machine": 34, "Mark": 35, "Mission": 36, "NumericRange": 37, "Object": 38, "Objective": 39, "Ordinal": 40, "Paused": 41, "Person": 42, "Plan": 43, "PlanContingency": 44, "Position": 45, "Predicate": 46, "QuaternionAttitude": 47, "Range": 48, "Resource": 49, "Role": 50, "Root": 51, "Scalar": 52, "Speed": 53, "State": 54, "Task": 55, "TaskTimeWindow": 56, "Text": 57, "Time": 58, "UnmannedVehicle": 59, "Vehicle": 60, "Velocity": 61, "WeatherLimits": 62} as const;
