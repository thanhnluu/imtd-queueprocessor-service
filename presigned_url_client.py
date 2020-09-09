import requests
import boto3
from botocore.exceptions import ClientError

class PresignedUrlClient:
    def __init__(self):
        pass


    def __str__(self):
        return "I am the presigned url client"


    def download_file(self, presignedUrl, file_path):
        file = requests.get(presignedUrl, allow_redirects=True)
        with open(file_path, "wb") as f:
            f.write(file.content)

    
    def upload_file(self, presigned_url, file_path):
        with open(file_path, "rb") as f:
            http_response = requests.put(presigned_url, data=f)
        return http_response.status_code

    
    """
    Only used to test upload and download using presigned urls
    """
    def create_presigned_upload_url(self, bucket_name, key):
        s3_client = boto3.client('s3')
        try:
            presigned_url = s3_client.generate_presigned_url('put_object', Params={"Bucket": bucket_name, "Key": key}, ExpiresIn=600)
        except ClientError as e:
            print(e)
            return None

        return presigned_url


    """
    Only used to test upload and download using presigned urls
    """
    def create_presigned_download_url(self, bucket_name, key):
        s3_client = boto3.client('s3')
        try:
            presigned_url = s3_client.generate_presigned_url('get_object', Params={"Bucket": bucket_name, "Key": key}, ExpiresIn=600)
        except ClientError as e:
            print(e)
            return None

        return presigned_url