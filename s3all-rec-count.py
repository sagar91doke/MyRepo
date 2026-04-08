import boto3

# Initialize S3 client
s3_client = boto3.client('s3')

# Replace with your S3 bucket name
S3_BUCKET = 'ih-webrtc-videos-mumbai'

def count_all_mp4_files(bucket_name):
    paginator = s3_client.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket_name)
    count = 0

    for page in pages:
        if 'Contents' in page:
            for obj in page['Contents']:
                file_name = obj['Key']
                if file_name.endswith('.mp4') and obj['Size'] > 0:
                    count += 1

    return count

if __name__ == "__main__":
    total_count = count_all_mp4_files(S3_BUCKET)
    print(f"🎥 Total MP4 recordings in bucket '{S3_BUCKET}': {total_count}")

