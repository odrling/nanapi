#!/bin/sh -xe
sudo chown -R $(id -u):$(id -g) .venv/ /poetry-cache/ /edgedb-config/ /edgedb-share/ /meilisearch/
mkdir -p ~/.config/ ~/.local/share/
ln -s /edgedb-config ~/.config/edgedb
ln -s /edgedb-share ~/.local/share/edgedb

curl -sSL https://install.python-poetry.org | python3 -
curl --proto '=https' --tlsv1.2 -sSf https://sh.edgedb.com | sh -s -- -y
curl -L https://install.meilisearch.com | (cd ~/.local/bin/ && sh)
