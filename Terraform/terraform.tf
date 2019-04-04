terraform {
    backend "s3" {
        encrypt = true
        bucket = ""
        key = ""
        access_key = ""
        secret_key = ""
        region = ""
    }
}