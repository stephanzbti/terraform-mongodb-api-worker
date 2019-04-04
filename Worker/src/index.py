import logging as log
from decouple import config
from src.controller.consumer.consumer import consumer as consumer

LOG_LEVEL = int(config('LOGGER_LEVEL', 10))


def initial():
    log.info('Starting ConsumerSQS')
    consumer()
    log.info('Starting ConsumerSQS')
