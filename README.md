# Serverless Chalice Application

The application uses Chalice to monitor a S3 bucket for object creations and standardise the country name column of each file with the ISO3166 standard. The file processed is automatically uploaded into a different bucket. It is also possible to both run the code and test the AWS deployment locally.

## Quick Start

The code contains three bash scripts that allow for a quick start of the application:

- run_app_localstack.sh
- run_docs.sh
- run_tests.sh

### run_app_localstack.sh
The script crates the docker container for LocalStack, creates the terraform scrip with infrastructure elements and applies it to the container. Afterwards, it start the application locally.

This enables tests to be done without provisioning resources on AWS and expending funds.

### run_docs.sh
The code is documented with doctoring in markdown format using pdoc3. This runs the documentation automatically.

### run_tests.sh
This scrip runs the pytests located in the code.


## Infrastructure 
The **AWS ** elements are created in **TerraFrom** using the 'main.tf' script, while the container with **LocalStack** is created with the 'docker-compose.yaml' file.

## Running the code on local files

It is also possible to run the standardisation on local files and folders. To do this, use the factory.py file that can be found in the chalicelib folder. 

## Create files and folders

The file explorer is accessible using the button in left corner of the navigation bar. You can create a new file by clicking the **New file** button in the file explorer. You can also create folders by clicking the **New folder** button.