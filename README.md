# OCCID2 semantic-product demo

Small executable demonstrator for adding semantic-product addressing to OCCID without replacing OCCID's normal model tree.

## Design boundary

There is one authored OCCID model hierarchy.

`parent:` continues to mean normal OCCID inheritance:

- descendants inherit fields from parents;
- concept ancestry remains meaningful;
- concepts and representations live in the same tree.

The semantic-product layer is an additional projection of meaning, not a second type hierarchy.

The demo intentionally does **not** contain:

- `struct`/`extends` serialization hierarchies;
- a giant `Action` axis;
- `GoHereTask`;
- `EntityState`;
- semantic `subject/property/role/focus/...` wrapper fields;
- pairwise `Machine disjoint Biological` rules.

## Task experiment

Surface task vocabulary remains ordinary enum vocabulary:

- `ManeuverIntent.MOVE`
- `ManeuverIntent.HOLD`
- `InformationIntent.LOCATE`
- `InformationIntent.TRACK`
- `InformationIntent.IDENTIFY`
- `InformationIntent.CLASSIFY`
- `EffectIntent.CREATE`
- `EffectIntent.REMOVE`

Those words compile into products of smaller semantic factors.

Example:

```text
MOVE
= Task
× Realm.WORLD
× TemporalMode.ACHIEVE
× Position
```

`TaskManeuver.intent` remains a real representation field because the intent varies per instance. The enum itself is not promoted to a universal semantic axis.

## Run

```bash
python compiler.py
python tests.py
python demo.py
```

Expected test result:

```text
14 tests passed
```

## Files

- `occid2.schema.yaml` - authored demo schema
- `compiler.py` - deterministic ahead-of-time compiler
- `runtime.py` - tiny semantic runtime/store
- `generated/occid2.py` - generated Python API
- `generated/semantic_registry.json` - inspectable generated semantic registry
- `demo.py` - worked examples
- `tests.py` - focused acceptance tests
- `SPEC.md` - standalone design specification
