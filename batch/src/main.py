import os
import argparse
import json
from google.cloud import batch_v1
from file_processing import process_jobs, clear_directory
from batch import create_job_request
import uuid

def main():
    parser = argparse.ArgumentParser(
                        prog='FloodModel',
                        description='Launches Cloud Batch jobs')   
    parser.add_argument('-p', '--project_id', default='climateiq-test')
    parser.add_argument('-r', '--region_id', default='us-central1')
    parser.add_argument('--template_name', default='citycat_template.json')
    parser.add_argument('--dry_run', action=argparse.BooleanOptionalAction)
    parser.add_argument('--study_area', default='studyarea-1')
    parser.add_argument('--config', default=1)
    parser.add_argument('--input_bucket',  default='citycat-input-test')
    parser.add_argument('--configuration_bucket', default='citycat-config-test')
    parser.add_argument('--output_bucket',  default='citycat-output-test')
    parser.add_argument('--memory', choices=range(16,129),type=int,help="Value must be between 16 and 128", default=96)

    args = parser.parse_args()
    print(f"Program arguments {args}")

    # Read in template batch job.
    batch_directory = os.path.dirname(os.path.dirname(__file__))
    with open(os.path.join(batch_directory, "template", args.template_name), 'r') as f:
        template = json.load(f)
        # Change the memory allocated.
        memory = str(int(args.memory * 1024)) 
        template["taskGroups"][0]["taskSpec"]["computeResource"]["memoryMib"] = memory
        template["allocationPolicy"]["instances"][0]["policy"]["machineType"] =  "e2-custom-32-" +memory

    # Read in the config.
    configs = []
    with open(os.path.join(batch_directory, "template", "config_" + str(args.config) + ".txt"), 'r') as f:
        for line in f.readlines():
            _,c,_,r = line.split()
            configs.append({"CityCat_Config": c,  "Rainfall_Data": r})

    # Deletes anything previously in jobs directory
    jobs_directory = os.path.join(batch_directory, "jobs")
    clear_directory(jobs_directory)

    for config in configs:
        c = config["CityCat_Config"]
        r = config["Rainfall_Data"]
        # Creates batch of jobs using the template
        job_uuid = uuid.uuid4().hex[:4]
        new_jobname = f"r{r}c{c}-{args.study_area}-config{args.config}-{job_uuid}"
        # Underscores are not valid in the job name. It must follow the regex: `^[a-z]([a-z0-9-]{0,61}[a-z0-9])?$`.
        # This replaces any underscores for hyphens.
        new_jobname = new_jobname.replace("_", "-") 
        with open(os.path.join(jobs_directory, f"{new_jobname}.json"), 'w') as f:
            # Modify the template, then dump it into the jobs folder
            new_job = template
            # Set the new job name
            new_job["name"] = new_jobname

            # Set environment variables
            env_varaibles = new_job["taskGroups"][0]["taskSpec"]["runnables"][0]["environment"]["variables"]
            env_varaibles["CITYCAT_CONFIG_FILE"] = c
            env_varaibles["RAINFALL_DATA_FILE"] = r
            env_varaibles["CONFIG"] = str(args.config)
            env_varaibles["STUDY_AREA"] = str(args.study_area)

            # Set buckets
            for volume in new_job["taskGroups"][0]["taskSpec"]["volumes"]:
                mountpath= volume["mountPath"]
                if (mountpath == "/mnt/disks/share/citycat-input-test"):
                    volume["gcs"]["remotePath"] = args.input_bucket
                elif (mountpath == "/mnt/disks/share/citycat-output-test"):
                    volume["gcs"]["remotePath"] = args.output_bucket
                elif (mountpath == "/mnt/disks/share/citycat-config-test"):
                    volume["gcs"]["remotePath"] = args.configuration_bucket

            json.dump(new_job, f, indent=1)

    jobs = process_jobs(jobs_directory)
    client = batch_v1.BatchServiceClient()

    for jobname, job in jobs.items():
        request = create_job_request(args.project_id, args.region_id, jobname, job)

        print(f"Job Name: {jobname}")
        if (not args.dry_run):
            try:
                job = client.create_job(request)
                print(f"{jobname} was succesfully created")
            except Exception as e:
                print(f"Error while trying to create job {jobname}: {e}")
    if not args.dry_run:
        print(f"Created {len(jobs)} jobs in Cloud Batch")

if __name__ == "__main__": 
    main()