!/bin/bash
/usr/local/bin/killport 10083
export NODE_HOME=/Users/imac/.nvm/versions/node/v16.10.0
export PATH=$NODE_HOME/bin:$PATH
make build-local
cp server/config.yaml ./build/

sed -in-place -e 's/8888/10088/g' ./build/config.yaml
