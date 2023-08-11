import logging

import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from boto3.session import Config

from django.conf import settings


# init logger
logger = logging.getLogger(__name__)


# Create a session and S3 client with custom configurations
# Access through IAM
session = boto3.Session()
s3 = session.client("s3",region_name='eu-central-1',config=Config(signature_version="s3v4"))


def getPresignedUrl(fileKey, expiration=3600, bucket=None):
    """
    Generates a pre-signed URL for downloading a file from the specified S3 bucket.

    :param fileKey: The key (path) of the file in the S3 bucket.
    :param expiration: Expiration time of the pre-signed URL in seconds.
    :param bucket: Optional parameter to specify a different bucket name.
    :return: Pre-signed URL for downloading the file, or False on error.
    """
    try:
        s3.head_object(Bucket=settings.BUCKET_NAME, Key=fileKey)
        response = s3.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket if bucket is not None else settings.BUCKET_NAME,
                                                            'Key': fileKey},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logger.error(f"Error generating pre-signed URL: {e}")
        return False

    return response


def storeFileInBucket(file, fileKey, bucket=None):
    """
    Stores a file object in the specified S3 bucket.

    :param file: The file object to be stored.
    :param fileKey: The key (path) to store the file in the S3 bucket.
    :param bucket: Optional parameter to specify a different bucket name.
    :return: 'DONE' if successful, or False on error.
    """
    try:
        s3.upload_fileobj(
            file,
            Bucket = bucket if bucket is not None else settings.BUCKET_NAME,
            Key = fileKey
        )
    except ClientError as e:
        logger.error(f"Error storing file in S3: {e}")
        return False
    
    return "DONE"