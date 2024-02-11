from pydantic import BaseModel


class Image(BaseModel):
    image_name: str
    width: int
    height: int
    extension: str
    path: str
