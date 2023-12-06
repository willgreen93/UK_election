from google.cloud import storage
from uk_election.params import LOCAL_DATA_PATH, GCP_PROJECT, BUCKET_NAME
import os
import asyncio

from prefect_gcp import GcpCredentials
from google.cloud import storage


async def load_google_credentials():
    gcp_credentials = await GcpCredentials.load("uk-elections")
    return gcp_credentials.get_cloud_storage_client(BUCKET_NAME)


async def load_data_from_gcp():
    os.makedirs(LOCAL_DATA_PATH, exist_ok=True)
    client = await load_google_credentials()
    bucket = client.bucket(BUCKET_NAME)
    files = bucket.list_blobs()
    file_names = [file.name for file in files]
    for file in file_names:
        blob = bucket.blob(file)
        blob.download_to_filename(os.path.join(LOCAL_DATA_PATH, file))


if __name__ == "__main__":
    asyncio.run(load_data_from_gcp())
