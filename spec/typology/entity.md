## Entity

[variants] by class:
- ACTOR: Actor
- MACHINE: Machine

Indicators [facets]:
- simulated flag
- exercise flag
- emergency flag
- c2 flag
- egressable flag
- starred flag

Override [facets]:
- field path being overridden
- override value
- status (OverrideStatus)
- type (OverrideType)
- expiry time

[enum] OverrideType:
- Live
- PostExpiry

[enum] CorrelationType:
- Manual
- Automated

[enum] CorrelationReplicationMode:
- Local
- Global

Correlation [facets]:
- primary entity
- secondary entities
- correlation type (CorrelationType)
- replication mode (CorrelationReplicationMode)

Decorrelation [facets]:
- decorrelated entity references
- reason
- timestamp

