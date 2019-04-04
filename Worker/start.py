import logging as log
from src.index import initial
from decouple import config

LOG_LEVEL = int(config('LOGGER_LEVEL', 10))

log.info('Starting Script WorkerSQS')

initial()

log.info('Finishing Script WorkerSQS')
