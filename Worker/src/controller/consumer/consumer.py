import boto3
from decouple import config
import logging as log
import base64
import json
import src.dao.sugestion as sugestions

BOTO3_AWS_KEY_ID = config('BOTO3_AWS_KEY_ID', '')
BOTO3_AWS_SECRET_KEY = config('BOTO3_AWS_SECRET_KEY', '')
BOTO3_AWS_REGION_NAME = config('BOTO3_AWS_REGION_NAME', '')
URLSQS = config('SQSURL', '')
LOG_LEVEL = int(config('LOGGER_LEVEL', 10))

log.basicConfig(format='%(levelname)s:%(message)s', level=LOG_LEVEL)

session = boto3.Session(
    aws_access_key_id=BOTO3_AWS_KEY_ID,
    aws_secret_access_key=BOTO3_AWS_SECRET_KEY,
    region_name=BOTO3_AWS_REGION_NAME
)

sqs = session.client(
    service_name='sqs',
    region_name=BOTO3_AWS_REGION_NAME,
    endpoint_url=URLSQS
)


def consumer():
    while True:
        try:
            responses = sqs.receive_message(
                QueueUrl=URLSQS,
                MaxNumberOfMessages=10,
                VisibilityTimeout=123,
                WaitTimeSeconds=10,
            )
            if 'Messages' in responses:
                for response in responses['Messages']:
                    log.debug(response)
                    sugestion = {
                        'messageId': response['MessageId'],
                        'message': response['Body']
                    }
                    sugestions.insert(sugestion)
                    responseDeleted = sqs.delete_message(
                        QueueUrl=URLSQS,
                        ReceiptHandle=response['ReceiptHandle']
                    )
                    log.debug(responseDeleted)
        except:
            log.debug('Problem Receiving Message')
