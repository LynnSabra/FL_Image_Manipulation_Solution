import os
import random
from Models.dataset import Dataset
from PIL import Image as PILImage

from services.dataset_service import DatasetService


class ImageBlackeningService:

    def __init__(self, dataset_service: DatasetService):
        self.dataset_service = dataset_service

    def blacken_image(self, image: PILImage):
        try:

            h, w = image.size
            image = image.convert("RGB")

            black = PILImage.new(str(image.mode), (h, w), 'black')
            result = PILImage.blend(image, black, 1)
            image.paste(result)
        except Exception as e:
            print(e)
            pass
        return image
#taking the dataset as an input
    def process_dataset(self, dataset: Dataset):
        for image_class in dataset.image_classes:
            for image in image_class.images:
                image_pil = PILImage.open(image.path)
                black_image = self.blacken_image(image_pil)
                self.dataset_service.save_image(image_pil=black_image, dataset_name=dataset.dataset_name, image_class=image_class.class_name, image=image)
        return os.path.join(self.dataset_service.get_output_dir(), dataset.dataset_name)

    def process_dataset_partial(self, dataset: Dataset, percentage: float):
        # temp_output_dir = self.dataset_service.create_temp_dir()
        # dataset_name = os.path.join(temp_output_dir, dataset.dataset_name)
        for image_class in dataset.image_classes:
            image_to_process = int(len(image_class.images) * percentage)
            # shuffle images and take first percentage of them
            image_to_process = random.sample(image_class.images, image_to_process)
            for image in image_class.images:
                if image in image_to_process:
                    image_pil = PILImage.open(image.path)
                    black_image = self.blacken_image(image_pil)
                    custom_image = image.copy()
                    custom_image.image_name = custom_image.image_name + "_blackened"
                    self.dataset_service.save_image(image_pil=black_image, dataset_name=dataset.dataset_name, image_class=image_class.class_name,
                                                    image=custom_image)
                # self.dataset_service.copy_image(output_dataset_name=dataset.dataset_name, image_class=image_class.class_name, image=image)
        return os.path.join(self.dataset_service.get_output_dir(), dataset.dataset_name)


if __name__ == "__main__":
    dataset_loader = DatasetService()
    image_blackening_service = ImageBlackeningService(dataset_service=dataset_loader)
    print(dataset_loader.list_datasets())
    dataset = dataset_loader.load_dataset("sample_dataset_1")
    # image_blackening_service.process_dataset(dataset)
    print(image_blackening_service.process_dataset_partial(dataset, 0.5))
