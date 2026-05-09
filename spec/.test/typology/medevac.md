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

