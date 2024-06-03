LOCATION="us-central1"
REPOSITORY="citycat-repository"

gcloud builds submit --region=${LOCATION} --tag ${LOCATION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/citycat-image:latest