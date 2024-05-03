# Batch job 

## Install the requirements

Create a virtual environment 
```
cd batch
python3 -m venv env
source env/bin/activate
pip install -r requirements. txt
```

## To run
```
cd batch
python3 src/main.py
python3 src/main.py --dry_run
python3 src/main.py --no-dry_run

# Set the study area and memory
python3 src/main.py --dry_run --study_area studyarea_2 --memory 128 --config 1
```

