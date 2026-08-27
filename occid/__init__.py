"""Canonical Python SDK namespace for OCCID.

Generated runtime models live in the repository's ``schema/`` source directory
and are installed as the ``occid.schema`` package. Consumers import them only
through ``occid`` so OCCID never competes with the common third-party package
named ``schema``.
"""

from __future__ import annotations

from . import schema

for _name in schema.__all__:
    globals()[_name] = getattr(schema, _name)

__all__ = [*schema.__all__, "schema"]
