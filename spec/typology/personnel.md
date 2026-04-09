# Personnel [Data → State of Person]

[enum] PersonnelStatusType:
- Present
- Absent
- WIA
- KIA
- MIA
- Captured
- Evacuated
- OnLeave
- Detached
- Hospitalized
- RTD

[enum] CasualtyCause:
- Combat
- NonCombat
- Accident
- Disease
- FriendlyFire

[enum] InjurySeverity:
- Minor
- Serious
- VSI
- Critical
- Fatal

[enum] TreatmentStatus:
- Untreated
- FirstAid
- Stabilized
- Evacuated
- Hospitalized
- RTD
- Deceased

PersonnelStatus [facets]:
- personnel status type
- effective time
- duty state

CasualtyReport [facets]:
- casualty cause
- injury severity
- treatment status
- evacuation status

---

# MEDEVAC [Control → Directive]

[enum] PrecedenceCategory:
- Urgent
- UrgentSurgical
- Priority
- Routine
- Convenience

[enum] SpecialEquipment:
- None
- Hoist
- ExtractionEquipment
- Ventilator

[enum] PatientType:
- Litter
- Ambulatory

[enum] SecurityAtPickup:
- NoEnemy
- PossibleEnemy
- EnemyInArea
- EnemyContact

[enum] MarkingMethod:
- Panels
- PyroSignal
- Smoke
- None
- Other
- IRStrobe
- VSPanel

[enum] CBRNEContamination:
- None
- Chemical
- Biological
- Radiological
- Nuclear

MEDEVACRequest [facets]:
- pickup zone
- patient precedence
- special equipment
- security at pickup
- marking method
- contamination state

