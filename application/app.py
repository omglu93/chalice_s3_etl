import io
import time
import boto3
from chalice import Chalice

from chalicelib.factory import lambda_name_standardization_factory
from chalicelib.iso3166.utils import load_to_s3
from chalicelib.core.config import settings

app = Chalice(app_name=settings.PROJECT_NAME)

s3_client = boto3.client(
    "s3",
    endpoint_url="http://host.docker.internal:4566",
    use_ssl=False,
    aws_access_key_id=settings.ACCESS_KEY,
    aws_secret_access_key=settings.SECRET_KEY,
    aws_session_token=settings.SESSION_TOKEN)


@app.on_s3_event(bucket=settings.INPUT_BUCKET, events=["s3:ObjectCreated:*"])
def handle_object_creation(event):
    # try:
    response = s3_client.get_object(Bucket=settings.INPUT_BUCKET,
                                    Key=event.key)

    with io.BytesIO(response['Body'].read()) as data:
        df1, df2 = lambda_name_standardization_factory(data=data,
                                                       file_name=event.key)
        # Load data to output bucket

        load_to_s3(s3_client=s3_client,
                   destination=settings.OUTPUT_BUCKET,
                   name="silver/{}".format(event.key),
                   dataframe=df1)

        # Load error report to bucket
        current_time = time.strftime("%Y%m%d-%H%M%S")
        load_to_s3(s3_client=s3_client,
                   destination=settings.OUTPUT_BUCKET,
                   name=f"error_report/{event.key}-{current_time}",
                   dataframe=df2)
