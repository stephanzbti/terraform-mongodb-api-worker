provider "aws" {
    access_key = ""
    secret_key = ""
    region = ""
}

resource "aws_sqs_queue" "terraform_queue"{
    name = "MaxMilhas_Queue"
    delay_seconds = 90
    max_message_size = 2048
    message_retention_seconds = 86400
    receive_wait_time_seconds = 10
    kms_master_key_id = "alias/aws/sqs"
    kms_data_key_reuse_period_seconds = 300

    tags = {
        Environment = "dev"
    }
}

