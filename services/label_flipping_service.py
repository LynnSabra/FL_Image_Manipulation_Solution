import os

from Models.dataset import Dataset
from services.dataset_service import DatasetService

#Dataset ad input
class LabelFlippingService:

    def __init__(self, dataset_service: DatasetService):
        self.output_folder = "output"
        self.dataset_service = dataset_service

    def process_dataset(self, dataset: Dataset):
        temp_output_dir = self.dataset_service.create_temp_dir()
        dataset_name = os.path.join(temp_output_dir, dataset.dataset_name)
        image_classes = dataset.image_classes.copy()
        image_classes_names = [image_class.class_name for image_class in image_classes]

        # right rotate image classes names
        image_classes_names = image_classes_names[-1:] + image_classes_names[:-1]

        custom_dataset = dataset.copy()
        for image_class, custom_image_class_name in zip(custom_dataset.image_classes, image_classes_names):
            custom_dataset.image_classes[custom_dataset.image_classes.index(image_class)].class_name = custom_image_class_name

        self.dataset_service.save_temp_dataset(custom_dataset, temp_output_dir)
        self.dataset_service.delete_dataset(os.path.join(dataset.dataset_name))
        self.dataset_service.copy_dataset(os.path.join(self.dataset_service.get_temp_output_dir(), temp_output_dir),
                                          os.path.join(self.dataset_service.get_output_dir(), dataset.dataset_name))
        return os.path.join(self.dataset_service.get_output_dir(), dataset.dataset_name)


if __name__ == '__main__':
    dataset_loader = DatasetService()
    label_flipping_service = LabelFlippingService(dataset_service=dataset_loader)
    print(dataset_loader.list_datasets())
    dataset = dataset_loader.load_dataset("sample_dataset_1")
    print(label_flipping_service.process_dataset(dataset))
