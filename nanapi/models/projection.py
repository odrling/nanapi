from pydantic import BaseModel

from nanapi.database.projection.projo_update_status import PROJO_UPDATE_STATUS_STATUS


class NewProjectionBody(BaseModel):
    name: str
    channel_id: int


class SetProjectionNameBody(BaseModel):
    name: str


class SetProjectionStatusBody(BaseModel):
    status: PROJO_UPDATE_STATUS_STATUS


class SetProjectionMessageIdBody(BaseModel):
    message_id: int


class ProjoAddExternalMediaBody(BaseModel):
    title: str
