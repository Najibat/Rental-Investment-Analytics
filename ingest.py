import os
import sys
import logging
import pandas as pd
import boto3
from dotenv import load_dotenv
from botocore.exceptions import ClientError
from datetime import datetime, timezone

# Ensure your config file exports AWS_REGION alongside credentials
from config import set_logger, ACCESS_KEY, SECRET_KEY, AWS_REGION

logger = set_logger()

S3_BUCKET_NAME = "ainowtaskaa"

# Cleaned mapping dictionary with fixed typos and correct casing options
FILES_MAPPING = {
    "january": {
        "candidate_keys": ["raw/Albany_listings_january.csv", "raw/albany_listings_january.csv"],
        "output_name": "data/Albany_listings_january.csv"
    },
    "february": {
        "candidate_keys": ["raw/albany_listings_february.csv", "raw/Albany_listings_february.csv"],
        "output_name": "data/albany_listings_february.csv"
    },
    "june": {
        "candidate_keys": ["raw/Albany_listings_june.csv", "raw/albany_listings_june.csv"],
        "output_name": "data/Albany_listings_june.csv"
    }
}


def get_s3_client():
    """Initializes AWS S3 Client using credentials and region from config."""
    if ACCESS_KEY and SECRET_KEY:
        return boto3.client(
            's3',
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
            region_name=AWS_REGION
        )
    else:
        logger.error("AWS credentials missing in configuration.")
        raise ValueError("AWS credentials missing.")


def fetch_and_save_csv(s3_client, candidate_keys, output_path, month_label):
    """Fetches a CSV from S3 and saves it directly to the local data/ directory."""
    for key in candidate_keys:
        try:
            logger.info(f"Downloading s3://{S3_BUCKET_NAME}/{key}...")
            obj = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=key)
            df = pd.read_csv(obj['Body'], low_memory=False)
            
            # Add ingestion metadata
            df['_snapshot_month'] = month_label
            df['_ingested_at'] = datetime.now(timezone.utc).isoformat()
            df['_source_file'] = f"s3://{S3_BUCKET_NAME}/{key}"
            df['ingestion_month'] ='january'
            
            # Ensure local output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Save raw file locally with correct name
            df.to_csv(output_path, index=False, encoding="utf-8")
            logger.info(f"Saved {len(df)} rows to '{output_path}' successfully.")
            return
            
        except ClientError as e:
            if e.response['Error']['Code'] in ['NoSuchKey', '404']:
                logger.warning(f"Key not found: '{key}'. Trying alternative key variation...")
                continue
            raise e

    raise FileNotFoundError(f"Could not find any matching keys in S3 for {month_label}: {candidate_keys}")


def run_ingestion():
    logger.info("========== Ingesting 3 Raw Files from S3 ==========")
    s3_client = get_s3_client()
    
    for month_label, file_info in FILES_MAPPING.items():
        fetch_and_save_csv(
            s3_client,
            file_info["candidate_keys"],
            file_info["output_name"],
            month_label
        )
        
    logger.info("========== Ingestion Complete! All 3 CSVs saved in data/ ==========")


if __name__ == "__main__":
    run_ingestion()

