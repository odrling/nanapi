# nanapi

## Clone nanapi

```sh
git clone https://git.japan7.bde.enseeiht.fr/Japan7/nanapi.git
```

## Setup EdgeDB

Follow the installation guide: https://www.edgedb.com/install

Launch and link an instance to the project:

```sh
cd nanapi/
edgedb project init
```

Web UI: `edgedb ui`

## Setup Meilisearch

```sh
docker run -d --name meilisearch -p 7700:7700 getmeili/meilisearch:latest
```

## Install and launch nanapi

```sh
poetry install
poetry shell
python -m nanapi
```

API docs: http://127.0.0.1/docs or http://127.0.0.1/redoc

## Dev Container

Dev Container config is also provided for VS Code.
