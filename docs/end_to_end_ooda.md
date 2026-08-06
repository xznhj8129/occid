# OCCID closed-loop command and control demonstration

## Purpose

This executable scenario is the reference demonstration for OCCID as a shared
semantic model for command, control, telemetry, operational reasoning, and
autonomous execution.

It is deliberately not a deployment demonstration. It does not require Sigma,
HiveLink, MPFC, MQTT, MAVLink, MSP, a flight controller, a network simulator, or
radio hardware. The only non-standard-library software dependency is OCCID.

The experiment isolates the claim being evaluated:

> Can one typed operational model carry a complete closed loop from observed
> state, through decision and directed action, to execution evidence and renewed
> operational state without collapsing identity, intent, tasking, planning,
> assignment, execution, telemetry, and observation into one protocol-specific
> message vocabulary?

## Scenario

A deterministic AI-CNC/OODA stand-in receives OCCID records describing:

- its own controller identity;
- an autonomous UAV identity;
- the UAV communication node and SENSOR/EFFECTOR roles;
- the UAV position and readiness as `EntityState`;
- its flight mode, phase, and battery state as `TelemetryState`.

The decision rule selects the UAV only when its identity, capability, readiness,
position, and energy satisfy the mission requirement.

It then creates a complete operational control chain:

1. `Objective` defines the desired end state and success criterion.
2. `IsrTask` defines the work required to satisfy that objective.
3. `Plan` defines the approved actor, route, step, and task relationship.
4. `Assignment` binds the task to the UAV under explicit authority.
5. `Execution` creates one independently tracked execution attempt.
6. `CommandMessage(ApplyPlanCommand)` directs the UAV to apply the plan.

The simulated autonomous executor validates those semantic relationships. It
then returns:

- assignment acceptance;
- execution start;
- task progress;
- updated entity and flight telemetry;
- a geolocated ISR observation;
- a track update and ISR result;
- completed task, execution, and assignment records;
- final vehicle state.

The decision agent evaluates the returned operational evidence and creates a new
revision of the same `Objective` with status `COMPLETE`.

## Application boundary

Every record crossing between a participant is processed by
`SemanticBoundary.transfer()`:

```text
OCCID model -> model.encode() -> bytes -> Model.decode() -> OCCID model
```

The boundary asserts exact model equality after decoding and records:

- OODA phase;
- source and destination participant;
- operational purpose;
- OCCID model name and permanent model ID;
- encoded byte count;
- complete named-field JSON representation.

The encoded byte count is recorded for reproducibility, not treated as the main
result. Transport selection, retries, routing, and radio behavior are outside the
scope of this experiment.

## Invariants

The run fails unless all of these properties hold:

1. Every application boundary completes an OCCID encode/decode round trip.
2. The UAV retains one stable entity identity across multiple state records.
3. `Objective`, `Task`, `Plan`, `Assignment`, and `Execution` remain distinct.
4. Their identifiers and references form one correlated control chain.
5. Runtime progress is expressed through `TaskDelta` and `Execution`, without
   mutating the original task or plan definitions.
6. Assignment acceptance is not treated as execution completion.
7. Telemetry and observations return to the decision system as OCCID records.
8. The objective is completed only after successful execution and geolocated ISR
   evidence are both present.

## Run

From the OCCID repository root:

```bash
python end_to_end_ooda.py
python end_to_end_ooda.py --json
python end_to_end_ooda.py --output /tmp/occid-ooda-trace.json
python -m unittest discover -s tests -p 'test_end_to_end_ooda.py'
```

The default output is a compact human-readable trace. `--json` and `--output`
produce the complete machine-readable experimental record suitable for paper
figures, tables, supplementary material, and regression comparison.

## What the scenario demonstrates

The scenario demonstrates an executable semantic lifecycle across:

- stable object identity;
- mutable telemetry and state;
- capability-based actor selection;
- objective formation;
- tasking and planning;
- assignment and authority;
- execution-attempt tracking;
- command dispatch;
- semantic acceptance;
- task and execution progress;
- ISR observation and track formation;
- evidence-based objective assessment;
- closure of the feedback loop.

## What it does not demonstrate

This experiment does not claim to validate:

- AI planning quality;
- flight-control behavior;
- radio or network performance;
- HiveLink routing or delivery policy;
- Sigma or MPFC deployment behavior;
- complete mappings to MAVLink, MSP, CoT, or other external standards;
- completeness or minimality of the entire OCCID ontology.

Those are separate integration and evaluation questions. This scenario exists to
make the OCCID semantic claim independently executable, inspectable, and
repeatable.
