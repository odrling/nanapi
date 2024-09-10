from pydantic import BaseModel


class ParticipantAddBody(BaseModel):
    participant_username: str
