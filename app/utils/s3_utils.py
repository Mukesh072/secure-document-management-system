import uuid
import boto3
from botocore.exceptions import ClientError
from flask import current_app


def get_s3_client():
    """
    Returns a boto3 S3 client.
    On EC2 with an IAM Role attached, boto3 auto-detects credentials -
    no keys needed. Locally, falls back to keys in .env if provided,
    or to `aws configure` credentials.
    """
    access_key = current_app.config.get("AWS_ACCESS_KEY_ID")
    secret_key = current_app.config.get("AWS_SECRET_ACCESS_KEY")
    region = current_app.config.get("AWS_REGION")
    print("Using AWS Region:", region)

    if access_key and secret_key:
        return boto3.client(
            "s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )
    return boto3.client("s3", region_name=region)


def generate_s3_key(user_id, filename):
    unique_id = uuid.uuid4().hex[:8]
    return f"user_{user_id}/{unique_id}_{filename}"


def upload_file_to_s3(file_obj, s3_key, content_type=None):
    s3 = get_s3_client()
    bucket = current_app.config["S3_BUCKET_NAME"]
    extra_args = {"ContentType": content_type} if content_type else {}
    try:
        s3.upload_fileobj(file_obj, bucket, s3_key, ExtraArgs=extra_args)
        return True
    except ClientError as e:
        current_app.logger.error(f"S3 upload failed for key {s3_key}: {e}")
        return False


def generate_presigned_url(s3_key, filename, expiration=300):
    """Generate a temporary secure download link (default 5 min)."""
    s3 = get_s3_client()
    bucket = current_app.config["S3_BUCKET_NAME"]

    try:
        url = s3.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": bucket,
                "Key": s3_key,
                "ResponseContentDisposition": f'attachment; filename="{filename}"'
            },
            ExpiresIn=expiration,
        )
        return url

    except ClientError as e:
        current_app.logger.error(f"Presigned URL generation failed for {s3_key}: {e}")
        return None


def delete_file_from_s3(s3_key):
    s3 = get_s3_client()
    bucket = current_app.config["S3_BUCKET_NAME"]
    try:
        s3.delete_object(Bucket=bucket, Key=s3_key)
        return True
    except ClientError as e:
        current_app.logger.error(f"S3 delete failed for key {s3_key}: {e}")
        return False
