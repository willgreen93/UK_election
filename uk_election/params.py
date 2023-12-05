import os

LOCAL_DATA_PATH = os.path.expanduser("~/.data_uk_election")

GCP_PROJECT = os.environ.get("GCP_PROJECT")
BUCKET_NAME = os.environ.get("BUCKET_NAME")
