"""Canonical Python SDK namespace for OCCID.

Generated runtime models still live in the repository's ``schema/`` directory,
but consumers import them through ``occid`` so OCCID never competes with the
common third-party package named ``schema``. The generated package is loaded as
``occid.schema`` and re-exported here.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path as _Path

_SCHEMA_PACKAGE = f"{__name__}.schema"
_SCHEMA_DIR = _Path(__file__).resolve().parent.parent / "schema"

_schema = sys.modules.get(_SCHEMA_PACKAGE)
if _schema is None:
    spec = importlib.util.spec_from_file_location(
        _SCHEMA_PACKAGE,
        _SCHEMA_DIR / "__init__.py",
        submodule_search_locations=[str(_SCHEMA_DIR)],
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"unable to load OCCID generated schema from {_SCHEMA_DIR}")
    _schema = importlib.util.module_from_spec(spec)
    sys.modules[_SCHEMA_PACKAGE] = _schema
    spec.loader.exec_module(_schema)

schema = _schema
for _name in schema.__all__:
    globals()[_name] = getattr(schema, _name)

__all__ = [*schema.__all__, "schema"]
