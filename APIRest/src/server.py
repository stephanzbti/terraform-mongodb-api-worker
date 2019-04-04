from flask import Flask, request
from flask_restful import Resource, Api
import json
from decouple import config
import logging as log
from src.controller.sqs.routes.sender import Sender

LOG_LEVEL = int(config('LOGGER_LEVEL', 10))
PORT = int(config('PORT', 3000))
DEFAULT = '/api/v1'

log.basicConfig(format='%(levelname)s:%(message)s', level=LOG_LEVEL)

app = Flask(__name__)
api = Api(app)

api.add_resource(Sender, DEFAULT+'/sender/sqs')


def initial():
    app.run(host='0.0.0.0', port=PORT)
