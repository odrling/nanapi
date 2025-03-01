# nanapi

## Develop with nanadev 🏠🍽️

One-click™ dev environment for nanapi and nanachan: https://github.com/Japan7/nanadev

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Japan7/nanadev)

## Develop locally

```sh
git clone https://github.com/Japan7/nanapi.git
cd nanapi/
```

### Setup Gel

Follow the installation guide: https://docs.geldata.com/learn/cli

Launch and link an instance to the project:

```sh
gel project init
```

Web UI: `gel ui`

### Setup Meilisearch

```sh
docker run -d --name meilisearch -p 7700:7700 getmeili/meilisearch:latest
```

## Local Settings

1. Copy [`nanapi/example.local_settings.py`](nanapi/example.local_settings.py) to `nanapi/local_settings.py`
2. Fill all the uncommented required variables

## Run nanapi

```sh
uv run --frozen -m nanapi
```

API docs: http://127.0.0.1/docs or http://127.0.0.1/redoc
