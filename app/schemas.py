from pydantic import BaseModel


class StrIds(BaseModel):
    ids: list[str]
