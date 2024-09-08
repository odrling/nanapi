from pydantic import BaseModel


class ParticipantAddBody(BaseModel):
    participant_id: int
    participant_username: str
