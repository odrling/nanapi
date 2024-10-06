# nanapi

## Clone nanapi

```sh
git clone https://github.com/Japan7/nanapi.git
cd nanapi/
```

## Setup EdgeDB

Follow the installation guide: https://www.edgedb.com/install

Launch and link an instance to the project:

```sh
edgedb project init
```

Web UI: `edgedb ui`

## Setup Meilisearch

```sh
docker run -d --name meilisearch -p 7700:7700 getmeili/meilisearch:latest
```

## Launch nanapi

```sh
uv run --frozen -m nanapi
```

API docs: http://127.0.0.1/docs or http://127.0.0.1/redoc
