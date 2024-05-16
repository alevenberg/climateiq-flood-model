LOCATION="us-central1"
PROJECT_ID="climateiq-test"
REPOSITORY="citycat-repo"

gcloud builds submit --region=${LOCATION} --tag ${LOCATION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/application-image:latest