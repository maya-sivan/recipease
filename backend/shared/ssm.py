import boto3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_ssm_parameter(name: str) -> str:
    ssm = boto3.client("ssm", region_name="us-west-2")
    try:
        param = ssm.get_parameter(Name=name, WithDecryption=True)
        value = param["Parameter"]["Value"]
        logger.info(f"SSM parameter {name} retrieved successfully")
        return value
    except Exception as e:
        logger.error(f"Error getting SSM parameter {name}: {e}")
        return None