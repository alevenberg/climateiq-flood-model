from google.cloud import batch_v1

def create_job_request(project_id: str, region: str, job_name: str, job: batch_v1.Job) ->batch_v1.CreateJobRequest:
    """
    This method takes a container job and creates a create job request

    Args:
        client: a cloud Batch client
        project_id: project ID or project number of the Cloud project you want to use.
        region: name of the region you want to use to run the job. Regions that are
            available for Batch are listed on: https://cloud.google.com/batch/docs/get-started#locations
        job_name: the name of the job that will be created.
            It needs to be unique for each project and region pair.

    Returns:
        A CreateJobRequest object for the job.
    """
    create_request = batch_v1.CreateJobRequest()
    create_request.job = job
    create_request.job_id = f"{job_name}"
    # The job's parent is the region in which the job will run
    create_request.parent = f"projects/{project_id}/locations/{region}"

    return create_request