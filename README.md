# Secure Document Management System Using AWS Cloud

Flask + SQLite + Amazon S3 + IAM + EC2 + CloudWatch.

## Local Setup

```bash
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # fill in S3_BUCKET_NAME, AWS_REGION, SECRET_KEY
python run.py
```

Visit http://127.0.0.1:5000

## AWS Setup Summary
1. Create S3 bucket (block public access ON).
2. Create IAM Role with S3 read/write policy scoped to that bucket.
3. Launch EC2 instance, attach the IAM Role.
4. Deploy code, run with Gunicorn + Nginx.
5. (Optional) Enable CloudWatch logging: set `ENABLE_CLOUDWATCH=true`.

Full step-by-step deployment instructions are provided separately in chat.
