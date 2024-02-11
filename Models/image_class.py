from pydantic import BaseModel
from typing import List, Optional

from Models.image import Image


class ImageClass(BaseModel):
    class_name: str
    class_path: str
    description: Optional[str]
    images: List[Image]

    def parse_class_name(self):
        return self.class_name
