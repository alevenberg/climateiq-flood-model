LOCATION="us-central1"
REPOSITORY="citycat-repository"

# Create the repository
gcloud artifacts repositories create ${REPOSITORY} \
    --repository-format=docker \
    --location=${LOCATION} \
    --description="Store the City Cat docker image" \
    --async