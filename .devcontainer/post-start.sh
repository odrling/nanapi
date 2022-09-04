#!/bin/sh -xe
poetry install

edgedb project info || edgedb project init --non-interactive
for INSTANCE in $(edgedb instance list --json | jq -r '.[].name'); do
    edgedb instance start -I $INSTANCE
done

nohup sh -c 'cd /meilisearch/ && meilisearch &' > meilisearch.out
