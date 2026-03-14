"""Shared tools available to any agent.

Add tools here that are broadly useful across multiple sub-agents
(e.g. BigQuery queries, GCS reads, Secret Manager lookups).

Usage in an agent:
    from ..shared_tools import query_bigquery, read_gcs_file
"""
from .bigquery import query_bigquery
from .gcs import read_gcs_file, write_gcs_file

__all__ = ["query_bigquery", "read_gcs_file", "write_gcs_file"]
