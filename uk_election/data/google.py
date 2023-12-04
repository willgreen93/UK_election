from google.cloud import storage
from uk_election.params import LOCAL_DATA_PATH
import os


def load_data_from_gcp():
    os.makedirs(LOCAL_DATA_PATH, exist_ok=True)
    client = storage.Client(project="uk-election-406413")
    bucket = client.bucket("ukelectiondata")
    files = bucket.list_blobs()
    file_names = [file.name for file in files]
    for file in file_names:
        blob = bucket.blob(file)
        blob.download_to_filename(os.path.join(LOCAL_DATA_PATH, file))


if __name__ == "__main__":
    load_data_from_gcp()
