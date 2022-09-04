from uuid import UUID

from edgedb import AsyncIOClient
from edgedb.errors import ConstraintViolationError
from fastapi import Depends, HTTPException, Response, status

from nanapi.database.histoire.histoire_delete_by_id import (
    HistoireDeleteByIdResult,
    histoire_delete_by_id,
)
from nanapi.database.histoire.histoire_get_by_id import HistoireGetByIdResult, histoire_get_by_id
from nanapi.database.histoire.histoire_insert import HistoireInsertResult, histoire_insert
from nanapi.database.histoire.histoire_select_id_title import (
    HistoireSelectIdTitleResult,
    histoire_select_id_title,
)
from nanapi.models.histoire import NewHistoireBody
from nanapi.utils.fastapi import HTTPExceptionModel, NanAPIRouter, get_client_edgedb

router = NanAPIRouter(prefix='/histoires', tags=['histoire'])


@router.oauth2_client.get('/', response_model=list[HistoireSelectIdTitleResult])
async def histoire_index(edgedb: AsyncIOClient = Depends(get_client_edgedb)):
    return await histoire_select_id_title(edgedb)


@router.oauth2_client_restricted.post(
    '/',
    response_model=HistoireInsertResult,
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_409_CONFLICT: dict(model=HTTPExceptionModel)})
async def new_histoire(body: NewHistoireBody,
                       edgedb: AsyncIOClient = Depends(get_client_edgedb)):
    try:
        return await histoire_insert(edgedb, **body.dict())
    except ConstraintViolationError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.oauth2_client.get(
    '/{id}',
    response_model=HistoireGetByIdResult,
    responses={status.HTTP_404_NOT_FOUND: dict(model=HTTPExceptionModel)})
async def get_histoire(id: UUID,
                       edgedb: AsyncIOClient = Depends(get_client_edgedb)):
    resp = await histoire_get_by_id(edgedb, id=id)
    if resp is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return resp


@router.oauth2_client_restricted.delete(
    '/{id}',
    response_model=HistoireDeleteByIdResult,
    responses={status.HTTP_204_NO_CONTENT: {}})
async def delete_histoire(id: UUID,
                          edgedb: AsyncIOClient = Depends(get_client_edgedb)):
    resp = await histoire_delete_by_id(edgedb, id=id)
    if resp is None:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return resp
