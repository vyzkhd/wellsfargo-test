from pydantic import BaseModel


class SampleData(BaseModel):
    id: int 
    x: list[int]
    y: list[int]