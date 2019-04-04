import boto3
from decouple import config
import logging as log
from flask_restful import Resource
from flask import request
import json

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

'''EndPoint: /api/v1/sender/sqs Tipo: 'POST'

Reponsável pelo envio ao SQS á mensagem de sugestão.
Payload: 
{
	"title": STRING, -> Titulo do Mensagem
	"author": STRING, -> Author do Mensagem
	"ttl": INT, -> Time to Leave, em semanas
	"message": STRING -> Mensagem da Mensagem
}
'''


class Sender(Resource):
    def post(self):
        try:
            log.debug('Starting request SenderSQS')

            data = request.data.decode()
            dataDict = json.loads(data)
            description = {
                'title': dataDict['title'],
                'author': dataDict['author'],
                'ttl': dataDict['ttl']
            }
            message = dataDict['message']

            log.debug('Calling function sendSQS')

            resp = sendSQS(description, message)

            log.debug('Stopping function sendSQS')
            if resp:
                log.debug('Stopping request SenderSQS')

                return {'success': 'SQS Sendend with success'}
            else:
                log.debug('Stopping request SenderSQS')

                return {'error': 'Problem sending'}
        except:
            log.error('Error Request SQS')
            return {'error': 'Problem sending'}


'''
Função sendSQS
Reponsável por enviar a mensagem para o SQS da AWS.

Parâmetros:
Description = {
    'title': STRING,
    author: STRING,
    'ttl': STRING
}

Message = STRING
'''


def sendSQS(description, message):
    try:
        log.debug('Starting request AWS SQS')

        response = sqs.send_message(
            QueueUrl=URLSQS,
            DelaySeconds=10,
            MessageAttributes={
                'Title': {
                    'DataType': 'String',
                    'StringValue': description['title']
                },
                'Author': {
                    'DataType': 'String',
                    'StringValue': description['author']
                },
                'WeeksOn': {
                    'DataType': 'Number',
                    'StringValue': description['ttl']
                }
            },
            MessageBody=(
                message
            )
        )

        log.debug(response)
        log.debug('Stoping request AWS SQS')
        return True
    except:
        log.debug('Problem request AWS SQS')
        return False
