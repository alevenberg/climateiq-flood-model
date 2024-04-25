# climateiq-flood-model
Runs CityCat flood model.

## Overview
The flood model is the CityCat.exe windows executable stored in a GCP bucket. To run CityCat, we containerize the application and run it using wine (a Windows simulator). Then we store the container in the Artifact Registry and run the container using Cloud Batch with mounted buckets.

## Containerize the application

### Build and run the image locally

### To build the image

```
cd citycat-image
DOCKER_BUILDKIT=1 docker build --tag=citycat-image:latest .
```

**Note**: Make sure you are in the correct directory when you try to build the image.

### To run

**Note**: You need to download the CityCat.exe and Domain_DESC.asc from the buckets before running the image.

The following mounts the 3 local directories and uses the default environment variables and entry point.
```
docker run -it -v $(pwd)/citycat-input-test:/mnt/disks/share/citycat-input-test -v $(pwd)/citycat-output-test:/mnt/disks/share/citycat-output-test -v $(pwd)/citycat-config-test:/mnt/disks/share/citycat-config-test citycat-image:latest 
```

CityCat is running correctly if you see something like the following:
```
0024:err:winediag:nodrv_CreateWindow Application tried to create a window, but no driver could be loaded.
0024:err:winediag:nodrv_CreateWindow L"Make sure that your X server is running and that $DISPLAY is set correctly."
--------------------------------------------------------
CityCat, version 6.4.11.7852, written by vassilis glenis
--------------------------------------------------------
```

#### Override env variables

Pass the command a `-e` flag.
```
docker run -it -e CITYCAT_CONFIG_FILE=2 -e RAINFALL_DATA_FILE=2 -v $(pwd)/citycat-input-test:/mnt/disks/share/citycat-input-test -v $(pwd)/citycat-output-test:/mnt/disks/share/citycat-output-test -v $(pwd)/citycat-config-test:/mnt/disks/share/citycat-config-test citycat-image:latest 
```

#### Enter the container

If you want to debug, it might be helpful to enter the container and override the entrypoint script by adding the flag `--entrypoint`.
```
docker run -it --entrypoint bash -v $(pwd)/citycat-input-test:/mnt/disks/share/citycat-input-test -v $(pwd)/citycat-output-test:/mnt/disks/share/citycat-output-test -v $(pwd)/citycat-config-test:/mnt/disks/share/citycat-config-test citycat-image:latest
```

To exit the container, type `exit`.

#### Troubleshooting

> If you make any changes to the Dockerfile or execute.sh script, you need to rebuild the image to see the changes.

<details>
  <summary>Verify the image was created</summary>
```
docker images citycat-image
```
</details>


