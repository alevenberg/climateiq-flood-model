import os
import json 
from google.cloud import batch_v1
from pathlib import Path

def process_jobs(directory):
    """
    Converts the .json files into Batch Job protos 

    Args:
        directory: the input directory that contains the batch job *.json files 
    """
    print(f"Processing input in directory `{directory}`...")
    files = [ f for f in os.listdir(directory) if f.endswith(".json") ]
    jobs = {}
    for file in files:
        with open(os.path.join(directory, file), 'r') as f:
            jobname= Path(file).stem
            job_json = json.loads(f.read()) 
            message = batch_v1.Job.from_json(json.dumps(job_json))
            jobs[jobname] = message

    return jobs

def clear_directory(directory):
    """
    Deletes all *.json files from a given directory

    Args:
        directory: the input directory that contains the *.json files 
    """
    print(f"Clearing input in directory `{directory}`...")
    files = [ f for f in os.listdir(directory) if f.endswith(".json") ]
    for file in files:
        os.remove(os.path.join(directory, file))