# climateiq-flood-model
Runs CityCat flood model.

## Overview
The flood model is the CityCat.exe windows executable stored in a GCP bucket. To run CityCat, we containerize the application and run it using wine (Windows simulator). Then, we store the container in the Artifact Registry and run the container using Cloud Batch with mounted buckets.

## Modifying the image and storing it in Cloud Batch 

[See instructions](./citycat_image/README.md)

## Running in Cloud Batch

[See instructions](./batch/README.md)

## Setting up GCP buckets with Terraform
[See instructions](./terraform/README.md)

## Config uploader
[See instructions](./config_uploader/README.md)