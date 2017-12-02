#!/usr/bin/env bash
docker stop mongodb bigchaindb
docker rm mongodb bigchaindb
rm -rf ../../../bigchaindb_docker/ ../../../mongodb_docker/
docker run   --interactive   --rm   --tty   --volume $HOME/bigchaindb_docker:/data   --env BIGCHAINDB_DATABASE_HOST=172.17.0.1   bigchaindb/bigchaindb   -y configure   mongodb
docker run   --detach   --name=mongodb   --publish=27017:27017   --restart=always   --volume=$HOME/mongodb_docker/db:/data/db   --volume=$HOME/mongodb_docker/configdb:/data/configdb   mongo:3.4.9 --replSet=bigchain-rs
docker run   --detach   --name=bigchaindb   --publish=59984:9984   --restart=always   --volume=$HOME/bigchaindb_docker:/data   bigchaindb/bigchaindb   start
python3 generate_fake_data.py
python3 competence.py