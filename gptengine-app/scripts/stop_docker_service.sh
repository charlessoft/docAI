#!/bin/bash
source ./config.sh
docker rm -f ${CONTAINER_NAME}
docker rm -f ${SCHEDULER_CONTAINER_NAME}
