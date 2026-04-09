# Supply Chain [Control → Directive + Data → State]

[enum] SupplyClass:
- I_Subsistence
- II_ClothingEquipment
- III_FuelPOL
- IV_Construction
- V_Ammunition
- VI_PersonalItems
- VII_MajorEndItems
- VIII_Medical
- IX_RepairParts
- X_Miscellaneous

[enum] SupplyPriority:
- Routine
- Priority
- Immediate
- Emergency

SupplyRequest [facets]:
- requested supply classes or items
- requested quantities
- destination
- required by time
- requesting unit

SupplyRoute [facets]:
- route geometry
- supported load classes
- threat level
- availability window

