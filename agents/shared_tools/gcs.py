"""Shared Cloud Storage tools."""


def read_gcs_file(bucket: str, blob_path: str) -> str:
    """Read a text file from Cloud Storage and return its contents.

    Args:
        bucket: GCS bucket name (without gs://).
        blob_path: Path to the file within the bucket.

    Returns:
        File contents as a string.
    """
    from google.cloud import storage

    client = storage.Client()
    blob = client.bucket(bucket).blob(blob_path)
    return blob.download_as_text()


def write_gcs_file(bucket: str, blob_path: str, content: str) -> str:
    """Write a string to a Cloud Storage file.

    Args:
        bucket: GCS bucket name (without gs://).
        blob_path: Destination path within the bucket.
        content: Text content to write.

    Returns:
        Confirmation message with the full GCS URI.
    """
    from google.cloud import storage

    client = storage.Client()
    blob = client.bucket(bucket).blob(blob_path)
    blob.upload_from_string(content, content_type="text/plain")
    return f"Written to gs://{bucket}/{blob_path}"
