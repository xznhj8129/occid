## Organization

[variants] by structure:
- GROUP: Group — contains subordinate organizations
- UNIT: Unit — contains only entities

[enum] OrgClass:
- Civilian
- Military
- Commercial
- NGO
- Unknown

[enum] CommandRelationship:
- OPCON — operational control
- TACON — tactical control
- ADCON — administrative control
- SUPCON — support
- DIRLAUTH — direct liaison authority

[enum] SupportRelationship:
- DirectSupport
- GeneralSupport
- Reinforcing
- GeneralSupportReinforcing

[enum] ArmyEchelon:
- FireTeam
- Squad
- Section
- Platoon
- Company
- Battery
- Troop
- Battalion
- Squadron
- Regiment
- Brigade
- Division
- Corps
- Army
- ArmyGroup
- Theater

[enum] UnitSize:
- IND
- TEM
- SQD
- SEC
- PLT
- COY
- BTN
- RGT
- BDE
- DIV
- FLT
- SQN
- GRP
- WNG

[enum] UnitCategory:
- COMB
- BATT
- TF
- MECH
- INF
- MOT
- REC
- UAV
- UAVA
- UAVR
- UGV
- SIG
- ENG
- ART
- MORT
- MRL
- ARM
- CAV
- MED
- SUP
- LOG
- HQ
- NBC
- MP
- AIR
- SOF
- NAV
- AMP
- ADA
- EW
- ISR
- CBT
- CSS
- COM
- DET
- RES
- TRG

[facets] all Organizations:
- org class (OrgClass)
- echelon (ArmyEchelon or UnitSize)
- taskforce flag (bool)
- national caveats
- interoperability level
- shared classification ceiling

Team [facets]:
- team identifier
- member entity references
- team lead entity reference
- purpose

