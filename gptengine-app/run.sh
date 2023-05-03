#!/bin/bash
docker run -it --rm -p8881:80 --name test \
    -v ${PWD}/textminer:/app/textminer \
    -v ${PWD}/uwsgi.ini:/app/uwsgi.ini \
    -v ${PWD}/logs:/app/logs \
    tm-textminer:latest /bin/sh
