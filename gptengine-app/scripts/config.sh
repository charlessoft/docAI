#!/bin/bash
PORT=18883
SCHEDULER_PORT=8889

# image name
APP_IMAGE_NAME=basin/gptengine-app

# image version
APP_IMAGE_VERSION=develop

# container name
CONTAINER_NAME=gptengine-app

# 调度 容器名
SCHEDULER_CONTAINER_NAME=apscheduler-app

# 调度地址 需要在host中配置域名
JOB_URL=http://textminer.job.url:8889/scheduler

#JOB_STORE=sqlite:////tmp/jobs.sqlite
