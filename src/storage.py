import json

from minio import Minio, S3Error
from src.config import settings

s3_client = Minio(
    settings.MINIO_ADDRESS, access_key=settings.MINIO_ROOT_USER, secret_key=settings.MINIO_ROOT_PASSWORD, secure=False
)


def s3_initialization():
    found = s3_client.bucket_exists(settings.MINIO_BUCKET_NAME)
    if not found:
        s3_client.make_bucket(settings.MINIO_BUCKET_NAME)

    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{settings.MINIO_BUCKET_NAME}/*",
            }
        ],
    }

    policy_json = json.dumps(policy)

    try:
        s3_client.set_bucket_policy(settings.MINIO_BUCKET_NAME, policy_json)
        print(f"Bucket {settings.MINIO_BUCKET_NAME} is now public.")
    except S3Error as e:
        print(f"Error setting bucket policy: {e}")
