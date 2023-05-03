#!/bin/bash
source ./config.sh

# ======
: ${LAMBDA_ROOT:=${PWD}}
: ${JENKINS_SSH_KEY_FOLDER:=${PWD}/ssh_key}
# ======

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


CMD_LIST=( harborcmd \
    )


#---------------
# 检测是否安装依赖命令行
#---------------
function check_depends_cmd(){
    for CMD in ${CMD_LIST[@]}
    do
        which ${CMD} > /dev/null 2>&1
        if [ $? -eq 0 ]
        then
            success "check ${CMD}"
        else
            echo "${CMD} no such file"
            exit 1
        fi

    done

}


function pull_imaegs(){
    harborcmd pull ${APP_IMAGE_NAME}:${APP_IMAGE_VERSION} ${APP_IMAGE_NAME}:${APP_IMAGE_VERSION}
    if [ $? -eq 0  ]; then
        success "harborcmd pull ${APP_IMAGE_NAME}:${APP_IMAGE_VERSION} "
    else
        error "harborcmd pull ${APP_IMAGE_NAME}:${APP_IMAGE_VERSION} "
    fi
}


check_depends_cmd
pull_imaegs

