import os
import random
from Models.dataset import Dataset
from services.dataset_service import DatasetService


class ImageShufflingService:
    def __init__(self, dataset_service: DatasetService):
        self.dataset_service = dataset_service

    def process_dataset(self, dataset: Dataset):
        temp_output_dir = self.dataset_service.create_temp_dir()
        dataset_name = os.path.join(temp_output_dir, dataset.dataset_name)
        temp_output_dir = os.path.join(temp_output_dir, dataset.dataset_name)
        images = []
        [images.extend(image_class.images) for image_class in dataset.image_classes]
        random.shuffle(images)
        custom_dataset = dataset.copy()

        for image_class in dataset.image_classes:
            total_images = image_class.images.__len__()
            custom_dataset.image_classes[dataset.image_classes.index(image_class)].images = images[:total_images]
            images = images[total_images:]

        self.dataset_service.save_temp_dataset(custom_dataset, temp_output_dir)
        self.dataset_service.delete_dataset(os.path.join(dataset.dataset_name))
        self.dataset_service.copy_dataset(os.path.join(self.dataset_service.get_temp_output_dir(), temp_output_dir),
                                          os.path.join(self.dataset_service.get_output_dir(), dataset.dataset_name))
        return os.path.join(self.dataset_service.get_output_dir(), dataset.dataset_name)


if __name__ == '__main__':
    dataset_loader = DatasetService()
    image_shuffling_service = ImageShufflingService(dataset_service=dataset_loader)
    print(dataset_loader.list_datasets())
    dataset = dataset_loader.load_dataset("sample_dataset_1")
    image_shuffling_service.process_dataset(dataset)
