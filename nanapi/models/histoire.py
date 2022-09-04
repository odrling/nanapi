from pydantic import BaseModel


class NewHistoireBody(BaseModel):
    title: str
    text: str
