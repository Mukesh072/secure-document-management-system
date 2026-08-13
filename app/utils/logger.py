import logging
import os
import boto3
from logging.handlers import RotatingFileHandler


def setup_logger(app):
    log_dir = os.path.join(app.root_path, "..", "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "app.log")

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    file_handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=3)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)

    # Optional: stream logs to AWS CloudWatch when running on EC2 with IAM role
    # Set ENABLE_CLOUDWATCH=true as an environment variable to activate.
    if os.environ.get("ENABLE_CLOUDWATCH", "false").lower() == "true":
        try:
            import watchtower

            cw_handler = watchtower.CloudWatchLogHandler(
    boto3_client=boto3.client(
        "logs",
        region_name=app.config["AWS_REGION"]
    ),
    log_group_name="secure-doc-management",
    stream_name="flask-app",
)
            cw_handler.setFormatter(formatter)
            app.logger.addHandler(cw_handler)
            app.logger.info("CloudWatch logging enabled.")
        except Exception as e:
            app.logger.warning(f"Could not enable CloudWatch logging: {e}")
