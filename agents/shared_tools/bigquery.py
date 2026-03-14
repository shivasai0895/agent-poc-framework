"""Shared BigQuery tool."""
import os


def query_bigquery(sql: str) -> list[dict]:
    """Run a BigQuery SQL query and return results as a list of row dicts.

    Args:
        sql: Standard SQL query string.

    Returns:
        List of rows, each row is a dict of column_name -> value.
    """
    from google.cloud import bigquery

    client = bigquery.Client(project=os.getenv("GOOGLE_CLOUD_PROJECT"))
    rows = client.query(sql).result()
    return [dict(row) for row in rows]
