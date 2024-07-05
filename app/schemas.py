from pydantic import BaseModel


class Ids(BaseModel):
    ids: list[int]
