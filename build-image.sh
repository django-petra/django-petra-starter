#! /bin/bash


if [ ! -e .env ]; then
    echo ".env file not found. Existing..."
    exit 1
fi

# Load Environment Variables
if [ -f .env ]; then
  set -o allexport
  source .env
  set +o allexport
fi


repository_name="django-petra-starter"
image_version="1.0.0"

export IMAGE_NAME="${repository_name}"
export IMAGE_TAG="${image_version}"

echo "Building Docker image..."
echo "====================================="

docker build \
 --platform="linux/amd64" \
 --file="docker/dockerfiles/app.Dockerfile" \
 --tag="${repository_name}:${image_version}" .


