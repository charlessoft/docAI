#!/bin/bash
image_name=basin/gptengine-app
version=latest


function build(){
    if [ ! -n "$1" ] ;then
        version=latest
        echo 'build ...latest'
    else
        version=$1
        version=${version//\//_}
        version=${version/master/latest}
        version=${version/orgin/}

    fi
    echo 'build version:' $version
    cd .. && \
        docker build  -t $image_name:$version .

}
build $*
