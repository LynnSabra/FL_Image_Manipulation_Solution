import os
import time

from Models.dataset import Dataset
from clients.picsum_image_client import PicSumImageClient
from services.dataset_service import DatasetService

#image replacement services that will be link to the image manipulation controller
#picsum API
class ImageReplacementService:
    def __init__(self, dataset_service: DatasetService, image_client: PicSumImageClient):
        self.dataset_service = dataset_service
        self.image_client = image_client

    def process_dataset(self, dataset: Dataset):
        # temp_output_dir = self.dataset_service.create_temp_dir()
        # dataset_name = os.path.join(temp_output_dir, dataset.dataset_name)
        for image_class in dataset.image_classes:
            for image in image_class.images:
                start = time.time()
                round_width, round_height = int(round(image.width / 100, 0) * 100), int(round(image.height / 100, 0) * 100)
                raw_image_content = self.image_client.get_image(width=round_width, height=round_height)
                self.dataset_service.save_byte_image(raw_image_content, dataset.dataset_name, image_class.class_name, image)
                del raw_image_content
                end = time.time()
                print(f"Image {image.image_name} processed in {end - start} seconds")
        return os.path.join(self.dataset_service.get_output_dir(), dataset.dataset_name)


if __name__ == '__main__':
    dataset_loader = DatasetService()
    image_client = PicSumImageClient()
    image_replacement_service = ImageReplacementService(dataset_loader, image_client)
    dataset = dataset_loader.load_dataset("sample_dataset_1")
    dataset_name = image_replacement_service.process_dataset(dataset)
    print(f"Dataset saved to {dataset_name}")
