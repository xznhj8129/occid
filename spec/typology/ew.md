# EW [Control → Process + Data → Intel]

[enum] EWActionType:
- Jam
- Spoof
- Deceive
- Intercept
- DirectionFind
- Monitor
- Deny

[enum] JamType:
- Noise
- Barrage
- Spot
- Sweep
- Responsive
- Follower

[enum] EWEffectType:
- SignalDegraded
- SignalDenied
- TargetDecoyed
- CommunicationsDisrupted
- NoEffect

[enum] EPType:
- FrequencyHopping
- SpreadSpectrum
- Encryption
- PowerControl
- DirectionalAntenna
- BurstTransmission

EWAction [facets]:
- EW action type
- target emitter or band
- start condition
- stop condition

DirectionFindingResult [facets]:
- emitter reference
- line of bearing
- confidence

