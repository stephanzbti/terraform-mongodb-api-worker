FROM python:3.7.3-alpine

ENV SQSURL https://sqs.us-east-1.amazonaws.com/588231123606/MaxMilhas
ENV BOTO3_AWS_KEY_ID AKIAYR5KOUKLK4K63YPH   
ENV BOTO3_AWS_SECRET_KEY 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
ENV BOTO3_AWS_REGION_NAME us-east-1
ENV LOGGER_LEVEL 10
ENV PORT 3000

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . .

RUN pip install -r requirements.txt

EXPOSE 3000

ENTRYPOINT ["python3", "start.py"]