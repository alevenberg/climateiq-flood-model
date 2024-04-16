from pathlib import Path
from glob import glob
import os
import sys
import argparse
import json
from google.protobuf.json_format import Parse, ParseDict
from google.cloud import batch_v1
from google.protobuf import json_format

# The script is going to do 3 things
# 1. Read in the input files from a bucket 
# 2. Set up and launch a city cat job for all the buckets
def get_flat_filename(file):
    basename = os.path.basename(file)
    flat_filename = []
    flat_filename.append(basename)
    fullname = os.path.dirname(file)
    basename = os.path.basename(fullname)
    while (basename != 'input'): 
        basename = os.path.basename(fullname)
        flat_filename.append(basename)
        fullname = os.path.dirname(fullname)
    return "".join(flat_filename[::-1])
 
# Reads the inputs from  and launches a batch job for each one
def process_jobs(directory):
    """
    This method launches the Cloud Batch jobs.

    Args:
    directory: the input directory that contains the batch job .json files 
    """
    print(f"Processing input in directory `{directory}`...")
    os.chdir(os.path.realpath(directory))
    files = Path(directory).glob('*.json')
    jobs = []
    for file in files:
        with open(file, 'r') as f:
            job_json = json.loads(f.read()) 
            message = batch_v1.Job.from_json(json.dumps(job_json))
            jobs.append(message)

    return jobs

 
def main():
    parser = argparse.ArgumentParser(
                        prog='FloodModel',
                        description='Launches Cloud Batch job')   
    parser.add_argument('-p', '--project_id', default='climateiq-test')
    parser.add_argument('-r', '--region_id', default='us-central1')
    # parser.add_argument('--input_bucket', required=True)
    # parser.add_argument('--configuration_bucket', required=True)
    # parser.add_argument('--output_bucket', required=True)

    args = parser.parse_args()
    print(args.project_id)

    # Change into the script directory.
    input_directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'input')
    jobs = process_input(input_directory)
    for job in jobs:
        pass
        # create_container_job(args.project_id, arg.region_id, "jobname", job)

if __name__ == "__main__": 
    main()