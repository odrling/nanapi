from pydantic import BaseModel

from nanapi.database.presence.presence_insert import PRESENCE_INSERT_TYPE


class NewPresenceBody(BaseModel):
    type: PRESENCE_INSERT_TYPE
    name: str
