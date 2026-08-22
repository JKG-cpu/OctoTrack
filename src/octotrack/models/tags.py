from pydantic import BaseModel

__all__ = ["Tag"]


class Tag(BaseModel):
    name: str
