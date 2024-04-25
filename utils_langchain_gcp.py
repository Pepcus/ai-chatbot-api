from dotenv import load_dotenv
from google.cloud import storage
from google.api_core.exceptions import NotFound
import os

load_dotenv()

def download_file_from_gcp(bucket_name, file_name):
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        local_file_path = os.environ['LOCAL_DOWNLOAD_PATH'] + file_name
        blob.download_to_filename(local_file_path)
        print(f"File downloaded from {bucket_name}/{file_name} to {local_file_path} successfully")
    except NotFound as e:
        print(f"Error: Object not found in bucket: {e}")
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")