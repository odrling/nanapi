from functools import cache
from typing import cast

import aiohttp
import edgedb
import meilisearch_python_sdk
import orjson
from meilisearch_python_sdk.json_handler import OrjsonHandler

from nanapi.settings import EDGEDB_CONFIG, MEILISEARCH_CONFIG, MEILISEARCH_HOST_URL


@cache
def get_edgedb() -> edgedb.AsyncIOClient:
    return _get_edgedb()


def _get_edgedb() -> edgedb.AsyncIOClient:
    client = edgedb.create_async_client(**EDGEDB_CONFIG)
    client = client.with_retry_options(
        edgedb.RetryOptions(attempts=300)
    )  # TODO: something more clever
    return cast(edgedb.AsyncIOClient, client)


def get_meilisearch() -> meilisearch_python_sdk.AsyncClient:
    client = meilisearch_python_sdk.AsyncClient(
        MEILISEARCH_HOST_URL, json_handler=OrjsonHandler(), **MEILISEARCH_CONFIG
    )
    return client


@cache
def get_session() -> aiohttp.ClientSession:
    timeout = aiohttp.ClientTimeout(total=30, connect=5, sock_connect=5)
    # until they fix https://github.com/aio-libs/aiohttp/issues/5975
    json_serialize = lambda d: orjson.dumps(d, option=orjson.OPT_SERIALIZE_NUMPY).decode()
    return aiohttp.ClientSession(timeout=timeout, json_serialize=json_serialize)
