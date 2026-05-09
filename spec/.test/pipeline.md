# Model Pipeline

This document is canonical for the build chain.

Format for authored schema is defined in `idl_spec.md`.

## Purpose

This model is built like source code, not like a notebook.

There are stable source files:
- `ontology.yaml`
- `vocabulary.yaml`
- `schema_src/*.yaml`

There are disposable build artifacts:
- `build/schema/*.yaml`
- `build/variants.yaml` if you want to inspect the expanded tree
- `build/ontology_tree.md` if you want a readable tree view

Generated files are never hand-edited.

## Stages

1. `ontology.yaml`
- The stable class tree
- Answers: what fundamentally exists?

2. `vocabulary.yaml`
- Unordered source vocabulary
- Candidate enum values and raw reference material
- Also the source of discriminator member lists
- Not structural truth

3. `build/variants.yaml`
- Generated expansion of ontology
- Answers: what concrete variant tree exists right now?

4. `schema_src/*.yaml`
- Hand-authored schema fragments
- Where fields, committed enums, maps, and helper structs are added
- Survives rebuilds

5. `build/schema/*.yaml`
- Generated merge of skeleton plus handwritten schema fragments
- Disposable

## Rules

- Ontology stays broad and stable
- Discriminator member lists are resolved from vocabulary
- Variants are generated, not authored
- Vocabulary is reference material, not tree structure
- Schema source is handwritten and preserved
- Build output is disposable

## Commands

Build the current variant tree:

```bash
python3 occid/spec/tools/build_variants.py
```

Build merged schema files:

```bash
python3 occid/spec/tools/build_schema.py
```

## Workflow

When changing the top of the model:
- edit `ontology.yaml`
- rebuild schema

When adding real IDL content:
- edit `schema_src/*.yaml`
- rebuild schema

This keeps top-down and bottom-up work separate while preserving handwritten schema work.
