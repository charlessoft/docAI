#!/bin/bash
source ./config.sh
# ======
: ${LAMBDA_ROOT:=${PWD}}

# Provide a variable with the location of this script.
#scriptPath="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
#echo $scriptPath

# Source Scripting Utilities
# -----------------------------------
# These shared utilities provide many functions which are needed to provide
# the functionality in this boilerplate. This script will fail if they can
# not be found.
# -----------------------------------

#utilsLocation="${scriptPath}/lib/utils.sh" # Update this path to find the utilities.
utilsLocation="${LAMBDA_ROOT}/lib/utils.sh"

if [ -f "${utilsLocation}" ]; then
  source "${utilsLocation}"
else
  echo "Please find the file util.sh and add a reference to it in this script. Exiting."
  echo 'utilsLocation:' ${utilsLocation}
  exit 1
fi
# ======

echo "docker run -d --name ${CONTAINER_NAME} -p ${PORT}:80 ${APP_IMAGE_NAME}:${APP_IMAGE_VERSION}"
docker run -d --name ${CONTAINER_NAME} -p ${PORT}:80 ${APP_IMAGE_NAME}:${APP_IMAGE_VERSION}
success "please open http://localhost:${PORT}/api/docs"

echo "================="
echo "docker run -d --name ${SCHEDULER_CONTAINER_NAME} -v ${PWD}/cache:/app/cache \
    -v ${PWD}/resources:/app/textminer/resources \
    -p ${SCHEDULER_PORT}:8889 \
    ${APP_IMAGE_NAME}:${APP_IMAGE_VERSION} /bin/bash -c 'python jobs/scheduler.py'"

docker run -d --name ${SCHEDULER_CONTAINER_NAME} -v ${PWD}/cache:/app/cache \
    -v ${PWD}/resources:/app/textminer/resources \
    -p ${SCHEDULER_PORT}:8889 \
    ${APP_IMAGE_NAME}:${APP_IMAGE_VERSION} /bin/bash -c 'python jobs/scheduler.py'
