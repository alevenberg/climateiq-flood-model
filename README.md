# climateiq-flood-model
Runs CityCat flood model.

## Overview
The flood model is the CityCat.exe windows executable stored in a GCP bucket. To run CityCat, we containerize the application and run it using wine (a Windows simulator). Then we store the container in the Artifact Registry and run the container using Cloud Batch with mounted buckets.

## Containerize the application

### Build and run the image locally

To build the image
```
sudo docker build --tag=citycat-image:1.0 .
```

To run
```
sudo docker run -it -v citycat-image:1.0 bash /execution/execute.sh
```

### Upload the image to the Artifact registry

## Bucket structure
The image expects 3 GCP buckets with the file structure:

- Input bucket
  - CityCat.exe
  - study_area1
    - Buildings.txt
    - Domain_DEM.asc
    - GreenAreas.txt
- Configuration bucket
  - config1
    - CityCat_Config_1.txt
    - CityCat_Config_2.txt
    - Rainfall_Data_1.txt
    - Rainfall_Data_2.txt
    - config_file (tells you what combinations of CityCat_Config and Rainfall_Data to use)
- Output bucket
  - config_1-rainfall_1-study area 
  - config_2-rainfall_1-study area 
