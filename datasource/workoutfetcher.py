import boto3
import botocore

Bucket = "Your S3 BucketName"
Key = "Name of the file in S3 that you want to download"
outPutName = "Output file name(The name you want to save after we download from s3)"

s3 = boto3.resource('s3')

try:
    s3.Bucket(Bucket).download_file(Key, outPutName)
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
        print("The object does not exist.")
    else:
        raise
