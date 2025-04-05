# hsa13-hw27-aws-serverless
Create Lambda function that will convert JPEG to BMP, GIF, PNG.

## Repo Structure

```
.
├── lambda_function.py             # Lambda function code
├── .gitignore
├── README.md
├── pillow-layer/
│   ├── Dockerfile                 # Docker for Pillow layer
│   └── build.sh                   # Build script
├── screenshots/                   # AWS screenshots
```

---

##  Implementation

###  Source bucket: `hsa13-hw27-image-converter-source-bucket`
###  Destination bucket: `hsa13-hw27-image-converter-destination-bucket`

---

## Lambda Configuration

- Runtime: Python 3.11
- Architecture: `arm64`
- Layer: Custom-built Pillow layer (compiled for Amazon Linux 2)
- Trigger: S3 `ObjectCreated:Put` event
- Environment variable:  
  `DEST_BUCKET=hsa13-hw27-image-converter-destination-bucket`

---

## Function Output Example

Uploaded: `converter-test.jpg`
```
Saved png/converter-test.png to hsa13-hw27-image-converter-destination-bucket
Saved gif/converter-test.gif to hsa13-hw27-image-converter-destination-bucket
Saved bmp/converter-test.bmp to hsa13-hw27-image-converter-destination-bucket
```


