"""
S3 Service for Evidence File Storage
"""

import boto3
from botocore.exceptions import ClientError
from datetime import datetime
import os

# Configuration from environment
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
S3_EVIDENCE_BUCKET = os.getenv("S3_EVIDENCE_BUCKET", "watchgraph-evidence-prod")

# Initialize S3 client
s3_client = boto3.client('s3', region_name=AWS_REGION)


def generate_s3_key(
    organization: str,
    system_id: str,
    requirement_mapping_id: str,
    filename: str
) -> str:
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    safe_filename = filename.replace("/", "_").replace("\\", "_")
    org = organization or "default"
    return f"{org}/{system_id}/{requirement_mapping_id}/{timestamp}_{safe_filename}"


def upload_file_to_s3(
    file_content: bytes,
    s3_key: str,
    content_type: str
) -> bool:
    try:
        s3_client.put_object(
            Bucket=S3_EVIDENCE_BUCKET,
            Key=s3_key,
            Body=file_content,
            ContentType=content_type,
            ServerSideEncryption='AES256',
        )
        print(f"✅ Uploaded {s3_key} to S3")
        return True
    except ClientError as e:
        print(f"❌ Failed to upload {s3_key} to S3: {e}")
        raise Exception(f"Failed to upload file: {str(e)}")


def generate_presigned_download_url(
    s3_key: str,
    filename: str,
    expires_in: int = 300
) -> str:
    try:
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': S3_EVIDENCE_BUCKET,
                'Key': s3_key,
                'ResponseContentDisposition': f'attachment; filename="{filename}"'
            },
            ExpiresIn=expires_in
        )
        return url
    except ClientError as e:
        print(f"❌ Failed to generate presigned URL for {s3_key}: {e}")
        raise Exception(f"Failed to generate download URL: {str(e)}")


def delete_file_from_s3(s3_key: str) -> bool:
    try:
        s3_client.delete_object(Bucket=S3_EVIDENCE_BUCKET, Key=s3_key)
        print(f"✅ Deleted {s3_key} from S3")
        return True
    except ClientError as e:
        print(f"❌ Failed to delete {s3_key} from S3: {e}")
        raise Exception(f"Failed to delete file: {str(e)}")


# MIME type mapping
MIME_TYPE_MAP = {
    "pdf": "application/pdf",
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "csv": "text/csv",
}

ALLOWED_FILE_TYPES = {"pdf", "png", "jpg", "jpeg", "xlsx", "docx", "csv"}
MAX_FILE_SIZE = 25 * 1024 * 1024  # 25MB
