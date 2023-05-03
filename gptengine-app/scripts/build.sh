#!/bin/bash

set -e
MASTER_ROOT=/mnt/yj-extract
mkdir -p ${MASTER_ROOT}
PYTHON_INSTAL_PATH=${MASTER_ROOT}/python3

function install_bzip(){
    echo "install_bzip"
    wget http://ci.basin.ali:2080/thirdparty/bzip/bzip2-1.0.6.tar.gz -O  bzip2-1.0.6.tar.gz
    tar zxvf bzip2-1.0.6.tar.gz && \
        cd bzip2-1.0.6/ && \
        make -f  Makefile-libbz2_so && \
        make && make install

}


function install_by3(){
    echo "install_py3"
    wget http://ci.basin.ali:2080/thirdparty/python/Python-3.6.6.tar.xz -O Python-3.6.6.tar.xz
    tar -Pxvf Python-3.6.6.tar.xz -C /tmp/ && \
        cd /tmp/Python-3.6.6 && \
        ./configure  --prefix=${PYTHON_INSTAL_PATH} && \
        make && \
        make install
   cd -

}

function install_requirement(){
    export PATH=${PYTHON_INSTAL_PATH}/bin:$PATH
#    ${PYTHON_INSTAL_PATH}/bin/pip3 install -r requestments.txt
    ${PYTHON_INSTAL_PATH}/bin/pip3 install -r requestments.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
}

function build_zip(){
    curpwd=${PWD}
    rm -fr *.xz
    rm -fr *.tar.gz
    cp -r ../yj-extract/ ${MASTER_ROOT}
    cd ${MASTER_ROOT}
    tar zcvf yj-extract.tar.gz yj-extract python3
    rm -fr yj-extractor
    mv  yj-extract.tar.gz ${curpwd}

    cd -

}


#yum install openssl-devel bzip2-devel expat-devel gdbm-devel readline-devel sqlite-devel gcc gcc-c++  openssl-devel

#install_bzip
install_by3
install_requirement
build_zip
