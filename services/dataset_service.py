import os
import shutil

import cv2
import datetime
from typing import List
from pathlib import Path
from PIL import Image as PILImage
from Models.dataset import Dataset
from Models.image import Image
from Models.image_class import ImageClass


class DatasetService:
    """
    This class is used to read the content of a dataset and parse them int dataset DTO
    """

    def __init__(self):
        self.dataset_root_folder: str = "datasets"
        self.dataset_output_folder: str = "datasets"
        self.dataset_temp_folder: str = "output"

    def list_datasets(self) -> List[str]:
        datasets = os.listdir(self.dataset_root_folder)
        return [dataset for dataset in datasets if os.path.isdir(os.path.join(self.dataset_root_folder, dataset))]

    def load_dataset(self, dataset_name) -> Dataset:
        dataset_path = os.path.join(self.dataset_root_folder, dataset_name)
        if not os.path.isdir(dataset_path):
            raise Exception(f"Dataset {dataset_name} not found")

        dataset = Dataset(dataset_name=dataset_name, path=dataset_path, image_classes=[])

        for image_class in os.listdir(dataset_path):
            image_class_path = os.path.join(dataset_path, image_class)
            if not os.path.isdir(image_class_path):
                continue

            image_class = ImageClass(class_name=image_class, class_path=image_class_path, description=None, images=[])
            for image in os.listdir(image_class_path):
                try:
                    image_path = os.path.join(image_class_path, image)
                    if not os.path.isfile(image_path):
                        continue

                    height, width = cv2.imread(image_path).shape[:2]
                    extension = os.path.splitext(image_path)[1]
                    image_class.images.append(Image(image_name=Path(image).stem, width=width, height=height, extension=extension, path=image_path))
                except Exception as e:
                    print(f"Error loading image {image_path}: {e}")
                    pass
            dataset.image_classes.append(image_class)

        return dataset

    def create_temp_dir(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_dir = os.path.join(self.dataset_temp_folder, timestamp)
        os.makedirs(temp_dir)
        return timestamp

    def get_output_dir(self) -> str:
        return self.dataset_output_folder

    def get_temp_output_dir(self) -> str:
        return self.dataset_temp_folder

    def copy_image(self, output_dataset_name: str, image_class: str, image: Image):
        output_dataset = os.path.join(self.dataset_output_folder, output_dataset_name, image_class)

        if not os.path.isdir(output_dataset):
            os.makedirs(output_dataset)

        shutil.copy(image.path, os.path.join(output_dataset, image.image_name + image.extension))

    def copy_image_temp(self, output_dataset_name: str, image_class: str, image: Image):
        output_dataset = os.path.join(self.dataset_temp_folder, output_dataset_name, image_class)
        if not os.path.isdir(output_dataset):
            os.makedirs(output_dataset)

        shutil.copy(image.path, os.path.join(output_dataset, image.image_name + image.extension))

    def save_image(self, image_pil: PILImage, dataset_name: str, image_class: str, image: Image):
        output_dataset = os.path.join(self.dataset_output_folder, dataset_name, image_class)

        if not os.path.isdir(output_dataset):
            os.makedirs(output_dataset)

        image_pil.save(os.path.join(output_dataset, image.image_name + image.extension))

    def save_byte_image(self, raw_image: bytes, dataset_name: str, image_class: str, image: Image):
        output_dataset = os.path.join(self.dataset_output_folder, dataset_name, image_class)

        if not os.path.isdir(output_dataset):
            os.makedirs(output_dataset)

        with open(os.path.join(output_dataset, image.image_name + image.extension), 'wb') as out_file:
            shutil.copyfileobj(raw_image, out_file)

    def save_dataset(self, dataset: Dataset, output_dataset_name: str):
        for image_class in dataset.image_classes:
            for image in image_class.images:
                self.copy_image(output_dataset_name, image_class.class_name, image)

    def save_temp_dataset(self, dataset: Dataset, output_dataset_name: str):
        for image_class in dataset.image_classes:
            for image in image_class.images:
                self.copy_image_temp(output_dataset_name, image_class.class_name, image)

    def delete_dataset(self, dataset_name):
        dataset_path = os.path.join(self.dataset_root_folder, dataset_name)
        shutil.rmtree(dataset_path)

    def copy_dataset(self, input_dir, output_dir):
        shutil.copytree(input_dir, output_dir)


if __name__ == '__main__':
    dataset_loader = DatasetService()
    print(dataset_loader.list_datasets())
    print(dataset_loader.load_dataset("sample_dataset_1"))
