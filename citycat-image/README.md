# Build and run the image locally

## To build the image

```
cd citycat-image
DOCKER_BUILDKIT=1 docker build --tag=citycat-image:latest .
```

**Note**: Make sure you are in the correct directory when you try to build the image.

## To run

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

### Override env variables

Pass the command a `-e` flag.
```
docker run -it -e CITYCAT_CONFIG_FILE=2 -e RAINFALL_DATA_FILE=2 -e STUDY_AREA=manhattan -v $(pwd)/citycat-input-test:/mnt/disks/share/citycat-input-test -v $(pwd)/citycat-output-test:/mnt/disks/share/citycat-output-test -v $(pwd)/citycat-config-test:/mnt/disks/share/citycat-config-test citycat-image:latest 
```


### Enter the container

If you want to debug, it might be helpful to enter the container and override the entrypoint script by adding the flag `--entrypoint`.
```
docker run -it --entrypoint bash -v $(pwd)/citycat-input-test:/mnt/disks/share/citycat-input-test -v $(pwd)/citycat-output-test:/mnt/disks/share/citycat-output-test -v $(pwd)/citycat-config-test:/mnt/disks/share/citycat-config-test citycat-image:latest
```

To exit the container, type `exit`.

### Troubleshooting

> If you make any changes to the Dockerfile or execute.sh script, you need to rebuild the image to see the changes.

<details>
  <summary>Verify the image was created</summary>
```
docker images citycat-image
```
</details>

# Storing the container in the Artifact Registry

1. [If it does not already exist] Create the artifact repository
2. Build the image
3. Tag and push the image to the artifact repository

## Create the artifact repository

Authorize via gcloud cli
```shell
PROJECT_ID=climateiq-test
gcloud auth login
gcloud config set project ${PROJECT_ID} 
```

Running the following script creates the repository: `citycat-repo`
```shell
chmod +x ./artifact-repository/create.sh 
./artifact-repository/create.sh
```

<details>
  <summary>To verify repo was created</summary>
```
gcloud artifacts repositories list
```
</details>

### Troubleshooting

<details>
  <summary>To delete a repo (if you want to change the name or create a new one)</summary>
```
gcloud artifacts repositories delete citycat-repo --location=us-central1
```
</details>

## Build the image
Using the steps above in [building the image locally](#to-build-the-image)

## Tag and push the image to the artifact repository

```
# Tag the image
TAG=tag4
docker tag citycat-image:latest us-central1-docker.pkg.dev/climateiq-test/citycat-repo/citycat-image:${TAG}

# Push the image
docker push us-central1-docker.pkg.dev/climateiq-test/citycat-repo/citycat-image:${TAG}
```
