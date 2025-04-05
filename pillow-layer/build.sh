#!/bin/bash

set -e

LAYER_NAME="pillow-layer"
PYTHON_VERSION="3.11"

rm -rf python layer ${LAYER_NAME}.zip

docker build -t ${LAYER_NAME} .

docker create --name tmp-container ${LAYER_NAME}

docker cp tmp-container:/opt/python ./python

docker rm tmp-container

zip -r ${LAYER_NAME}.zip python

echo "Done. Created ${LAYER_NAME}.zip"