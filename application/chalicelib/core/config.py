from os import getenv
from dotenv import main

main.load_dotenv()


class ApplicationSettings:

    PROJECT_NAME: str = "ISO-3166-Standardizer"
    INPUT_BUCKET: str = getenv("INPUT_BUCKET_NAME")
    OUTPUT_BUCKET: str = getenv("OUTPUT_BUCKET_NAME")


settings = ApplicationSettings()
