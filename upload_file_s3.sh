#! /usr/bin/env bash

aws --endpoint-url=http://localhost:4566 s3 cp test.txt s3://data-input-bucket
aws --endpoint-url=http://localhost:4566 s3 ls s3://data-input-bucket
