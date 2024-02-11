from pydantic import BaseModel
from typing import List

from Models.image_class import ImageClass


class Dataset(BaseModel):
    dataset_name: str
    path: str
    image_classes: List[ImageClass]

    def parse_image_classes(self):
        return [image_class.parse_class_name() for image_class in self.image_classes]

    def filter_image_class(self, class_name):
        return [image_class for image_class in self.image_classes if image_class.class_name == class_name][0]
