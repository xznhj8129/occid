### Intel

#### Detection

Detection [facets]:
- position (where)
- timestamp (when)
- confidence (float 0-1)

[variants] by sensor:
- ACOUSTIC: AcousticDetection
- MOTION: MotionDetection
- SEISMIC: SeismicDetection
- CBRNE: CBRNEDetection
- LAUNCH: LaunchDetection
- IMPACT: ImpactDetection
- VIDEO: VideoDetection
- RADAR: RadarDetection
- RF: RFDetection

VideoDetection [facets]:
- bounding box (x, y, w, h)
- class id, class name
- confidence
- track id

#### Classification

Classification [facets]:
- detection reference (what was detected)
- assessed type/category
- confidence
- method

[enum] PIDMethod:
- Visual
- Electronic
- Behavioral
- Intelligence

#### Track

Track [facets]:
- detection reference or track ID
- position history or current estimated state
- confidence

[facets] extended:
- track quality score (0-15)
- sensor hits count
- last measurement time
- line of bearing
- radar cross section (dBsm)
- number of objects (range)

[enum] TrackState:
- Tentative
- Confirmed
- Coasting
- Dropped

#### Assessment

##### BDA (Battle Damage Assessment)

BDAResult [facets]:
- target reference
- assessment time
- assessor
- method (BDAMethod)
- phase (BDAPhase)
- damage level (DamageLevel)
- functional impact (FunctionalImpact)
- confidence
- restrike recommendation
- imagery reference

[enum] BDAMethod:
- Visual
- ElectroOptical
- Infrared
- Radar
- SignalIntel
- HumanIntel

[enum] BDAPhase:
- Phase1_Initial
- Phase2_Supplemental
- Phase3_Restrike

[enum] DamageLevel:
- Undamaged
- Light
- Moderate
- Heavy
- Destroyed

[enum] FunctionalImpact:
- FullyOperational
- Degraded
- SignificantlyDegraded
- NonOperational
- Destroyed

[enum] BDAStatusColor:
- Grey
- Yellow
- Green
- Red

[enum] IntelDiscipline:
- HUMINT
- SIGINT
- OSINT
- GEOINT
- MASINT

[enum] SIGINTType:
- COMINT
- ELINT
- FISINT

IntelReport [facets]:
- report identifier
- classification
- intelligence discipline (IntelDiscipline)
- DTG
- content summary
- reliability rating
- credibility rating

HUMINTReport [facets]:
- source reliability
- information credibility
- source identifier
- handler reference

SIGINTReport [facets]:
- SIGINT type (SIGINTType)
- intercept time
- emitter reference
- content summary

OSINTReport [facets]:
- source URL
- source type
- access time
- relevance score

GEOINTReport [facets]:
- imagery reference
- coverage area
- resolution
- collection time
- source platform

MASINTReport [facets]:
- measurement type
- sensor type
- data reference
- analysis summary

##### Target Management (Assessment)

HighValueTarget [facets]:
- is high value (bool)
- priority (int, lower = higher)
- is high payoff (bool)
- target matches

HighValueTargetMatch [facets]:
- high value target reference
- match confidence
- match time
- matching criteria

TargetPriority [facets]:
- high value target info
- threat assessment (is_threat bool)

[enum] IPBType:
- TerrainAnalysis
- WeatherAnalysis
- ThreatEvaluation
- ThreatIntegration
- CourseOfActionDevelopment

IPBProduct [facets]:
- IPB product type (IPBType)
- area of operations
- prepared date
- prepared by

CommonOperatingPicture [facets]:
- timestamp
- entities
- tracks
- events
- area of operations

RecognizedAirPicture [facets]:
- timestamp
- air tracks
- airspace status

RecognizedMaritimePicture [facets]:
- timestamp
- maritime tracks
- maritime status

HighValueTargetList [facets]:
- ordered targets
- justification

HighPayoffTargetList [facets]:
- ordered targets
- engagement criteria

NoStrikeList [facets]:
- protected entities or sites
- reasons

##### Intelligence Reliability (Assessment)

[enum] SourceReliability:
- A_CompletelyReliable
- B_UsuallyReliable
- C_FairlyReliable
- D_NotUsuallyReliable
- E_Unreliable
- F_CannotBeJudged

[enum] InfoCredibility:
- 1_Confirmed
- 2_ProbablyTrue
- 3_PossiblyTrue
- 4_Doubtful
- 5_Improbable
- 6_CannotBeJudged

#### Fusion

[enum] FusionMethod:
- NearestNeighbor
- Bayesian
- DempsterShafer
- KalmanFilter
- CovarianceIntersection
- Voting
- WeightedAverage

[enum] FusionLevel:
- L0_SourcePreprocessing
- L1_ObjectAssessment
- L2_SituationAssessment
- L3_ImpactAssessment
- L4_ProcessRefinement

[enum] GateType:
- Rectangular
- Ellipsoidal
- Mahalanobis

