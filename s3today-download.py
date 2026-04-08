import boto3
import os
import zipfile
from datetime import date

# Initialize S3 client
s3_client = boto3.client('s3')

# Replace with your S3 bucket name
S3_BUCKET = 'ih-webrtc-videos-mumbai'

# Get today's date
from datetime import date, datetime

# Set a fixed date manually
today = datetime.strptime("2025-12-09", "%Y-%m-%d").date()
today_str = today.strftime("%Y-%m-%d")

#start_date = datetime.strptime("2025-10-28", "%Y-%m-%d").date()
#end_date = datetime.strptime("2025-10-31", "%Y-%m-%d").date()


# Local download directory
download_dir = "downloads"
os.makedirs(download_dir, exist_ok=True)

count = 0
downloaded_files = []
paginator = s3_client.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=S3_BUCKET)

def get_unique_filename(directory, filename):
    """Ensure filename is unique in directory by appending a counter if needed."""
    base, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{base}_{counter}{ext}"
        counter += 1
    return new_filename

for page in pages:
    if 'Contents' in page:
        for obj in page['Contents']:
            if obj['Size'] > 0:
                last_modified_date = obj['LastModified'].date()
                file_name = obj['Key']

                if file_name.endswith('.mp4') and last_modified_date == today:
                    count += 1
                    original_filename = os.path.basename(file_name)
                    
                    # Add today's date to filename
                    base, ext = os.path.splitext(original_filename)
                    dated_filename = f"{base}_{today_str}{ext}"
                    
                    # Ensure uniqueness
                    safe_filename = get_unique_filename(download_dir, dated_filename)
                    local_file_path = os.path.join(download_dir, safe_filename)

                    print(f"Downloading {file_name} to {local_file_path}...")
                    s3_client.download_file(S3_BUCKET, file_name, local_file_path)
                    downloaded_files.append(local_file_path)

# Zip all downloaded files
if downloaded_files:
    zip_filename = f"recordings_{today_str}.zip"
    zip_filepath = os.path.join(download_dir, zip_filename)
    with zipfile.ZipFile(zip_filepath, 'w') as zipf:
        for file in downloaded_files:
            zipf.write(file, os.path.basename(file))

    print(f"\n✅ A total of {count} MP4 files were downloaded and zipped into {zip_filepath}")
else:
    print(f"\n⚠️ No MP4 recordings found for {today_str}")

