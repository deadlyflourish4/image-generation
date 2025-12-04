from google.cloud import storage
from datetime import timedelta
import os

GCS_BUCKET = os.getenv("GCS_BUCKET", "your-bucket-name")

storage_client = storage.Client()

def generate_signed_upload_url(task_id: str, expires_minutes: int = 15):
    bucket = storage_client.bucket(GCS_BUCKET)

    object_name = f"input/{task_id}.png"
    blob = bucket.blob(object_name)

    url = blob.generate_signed_url(
        version="v4",
        expiration=timedelta(minutes=expires_minutes),
        method="PUT",
        content_type="image/png",
    )

    return url
