# Batch job 

## Install the requirements
- [ ] [gcloud CLI](https://cloud.google.com/sdk/docs/install)
- [ ] [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

### Make sure the repo is update
```
git pull upstream main
```

### Create a virtual environment 

#### For linux
```
cd batch
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

#### For windows 

```
cd batch
py -m venv env
env\Scripts\activate
py -m pip install -r requirements.txt
```

### Install gcloud CLI

Follow [instructions](https://cloud.google.com/sdk/docs/install-sdk)

Verify using

```
gcloud --help
```

Authenticate using:
```
gcloud auth application-default login
```

## To run

### For linux

```
cd batch
python3 src/main.py
python3 src/main.py --dry_run
python3 src/main.py --no-dry_run

# Set the study area and memory
python3 src/main.py --dry_run --study_area studyarea_2 --memory 128 --config 1
```
### For windows 

```
cd batch
py src/main.py
py src/main.py --dry_run
py src/main.py --no-dry_run

# Set the study area and memory
py src/main.py --dry_run --study_area studyarea_2 --memory 128 --config 1
```

## To cancel a job
```
gcloud batch jobs delete --location=us-central1 <job_name>
```

## To get information about a job
```
gcloud batch jobs describe studyarea-2 --location=us-central1
```