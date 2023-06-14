import boto3

from typing import BytesIO

class S3Service:
    def __inti__(self):
        self.s3 = boto3.client("s3")

    def upload_file(self, file: BytesIO, filename:str):
        bucket = "inabat.akanova-bucket"
        filekey = f"shanyraks/{filename}"
        self.s3.upload_fileobj(file, bucket, filekey)