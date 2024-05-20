LOCATION="us-central1"
PROJECT_ID="climateiq-test"
REPOSITORY="citycat-repo"

# Create the repository
gcloud artifacts repositories create ${REPOSITORY} \
    --repository-format=docker \
    --location=${LOCATION} \
    --description="Store the City Cat docker image" \
    --async