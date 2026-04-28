"""
Local cache engine for OPE_DB_API client-side PostgreSQL.

Responsibilities:
- Coordinate initial sync
- Incremental history sync
- Snapshot (hierarchy) sync
- Cache maintenance (clear / reset)

This package is domain-agnostic and registry-driven.
"""
