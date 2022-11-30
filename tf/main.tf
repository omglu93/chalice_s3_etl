provider "aws" {
  access_key                  = "mock_access_key"
  secret_key                  = "mock_secret_key"
  region                      = "us-east-1"
  s3_use_path_style           = true
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  insecure                    = true

  endpoints {
    iam              = "http://localhost:4566"
    lambda           = "http://localhost:4566"
    s3               = "http://localhost:4566"
  }
}

resource "aws_s3_bucket" "test-input-bucket" {
  bucket = "data-input-bucket"
}

resource "aws_s3_bucket" "test-output-bucket" {
  bucket = "data-output-bucket"
}

resource "aws_iam_role" "invocation_role" {
  name = "api_gateway_auth_invocation"
  path = "/"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": {
    "Effect": "Allow",
    "Action": "s3:ListBucket",
    "Resource": "arn:aws:s3:::test-bucket"
  }
}
EOF
}