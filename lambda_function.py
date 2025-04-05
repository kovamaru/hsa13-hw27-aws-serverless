import boto3
import os
from PIL import Image
from io import BytesIO

s3 = boto3.client('s3')

def lambda_handler(event, context):
  print(f"Received event: {event}")

  try:
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
  except Exception as e:
    print(f"Error parsing event: {e}")
    return {"status": "error", "reason": "invalid event"}

  if not key.lower().endswith((".jpeg", ".jpg")):
    print(f"Skipped file: {key} (not a JPEG/JPG)")
    return {"status": "skipped", "file": key}

  try:
    response = s3.get_object(Bucket=bucket, Key=key)
    image_data = response['Body'].read()
    img = Image.open(BytesIO(image_data))
  except Exception as e:
    print(f"Error reading image from S3: {e}")
    return {"status": "error", "reason": "failed to read image"}

  dest_bucket = os.environ.get('DEST_BUCKET')
  if not dest_bucket:
    print("DEST_BUCKET environment variable not set")
    return {"status": "error", "reason": "missing DEST_BUCKET"}

  formats = ['PNG', 'GIF', 'BMP']
  base_filename = key.rsplit('.', 1)[0]

  for fmt in formats:
    try:
      out_buffer = BytesIO()
      img.save(out_buffer, fmt)
      out_buffer.seek(0)

      dest_key = f"{fmt.lower()}/{base_filename}.{fmt.lower()}"
      content_type = f"image/{'jpeg' if fmt == 'JPG' else fmt.lower()}"

      s3.put_object(
          Bucket=dest_bucket,
          Key=dest_key,
          Body=out_buffer,
          ContentType=content_type
      )
      print(f"Saved {dest_key} to {dest_bucket}")
    except Exception as e:
      print(f"Error converting to {fmt}: {e}")

  return {"status": "converted", "file": key}