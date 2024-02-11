from typing import List

from fastapi import APIRouter, HTTPException

from Models.dataset import Dataset
from Models.image_class import ImageClass
from services.dataset_service import DatasetService

router = APIRouter()
dataset_service = DatasetService()


@router.get("/", response_model=List[str])
def get_datasets():
    try:
        return dataset_service.list_datasets()
    except Exception as e:
        return HTTPException(status_code=400, detail=e.__str__())


@router.get("/{dataset_name}", response_model=Dataset)
def get_dataset_details(dataset_name: str):
    try:
        return dataset_service.load_dataset(dataset_name)
    except Exception as e:
        return HTTPException(status_code=404, detail=e.__str__())


@router.get("/{dataset_name}/classes", response_model=List[str])
def get_dataset_classes(dataset_name: str):
    try:
        return dataset_service.load_dataset(dataset_name).parse_image_classes()
    except Exception as e:
        return HTTPException(status_code=404, detail=e.__str__())


@router.get("/{dataset_name}/classes/{class_name}", response_model=ImageClass)
def get_class_images(dataset_name: str, class_name: str):
    try:
        return dataset_service.load_dataset(dataset_name).filter_image_class(class_name)
    except Exception as e:
        return HTTPException(status_code=404, detail=e.__str__())
