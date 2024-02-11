from fastapi import APIRouter, HTTPException
from starlette.responses import FileResponse
from clients.picsum_image_client import PicSumImageClient
from services.dataset_archive_service import DatasetArchiveService
from services.dataset_service import DatasetService
from services.image_blackening_service import ImageBlackeningService
# from services.image_blurring_service import ImageBlurringService
from services.image_replacement_service import ImageReplacementService
from services.image_shuffling_service import ImageShufflingService
from services.label_flipping_service import LabelFlippingService

router = APIRouter()
dataset_service = DatasetService()
image_client = PicSumImageClient()
dataset_archive_service = DatasetArchiveService()
image_blackening_service = ImageBlackeningService(dataset_service)
image_replacement_service = ImageReplacementService(dataset_service=dataset_service, image_client=image_client)
image_shuffling_service = ImageShufflingService(dataset_service=dataset_service)
label_flipping_service = LabelFlippingService(dataset_service=dataset_service)


@router.get("/image/blackening/{dataset_name}")
def blacken_images(dataset_name: str):
    try:
        dataset = dataset_service.load_dataset(dataset_name)
        output_dataset = image_blackening_service.process_dataset(dataset)

        # archive_path = dataset_archive_service.create_archive(folder_to_compress=output_dataset, archive_name=output_dataset.split('/')[0])
        # return FileResponse(archive_path, media_type="application/zip", filename=f"{dataset_name}.zip")
        return output_dataset
    except Exception as e:
        return HTTPException(status_code=404, detail=e.__str__())


@router.get("/image/blackening/{dataset_name}/{percentage}")
def blacken_images_by_percentage(dataset_name: str, percentage: float):
    try:
        dataset = dataset_service.load_dataset(dataset_name)
        output_dataset = image_blackening_service.process_dataset_partial(dataset, percentage)

        # archive_path = dataset_archive_service.create_archive(folder_to_compress=output_dataset, archive_name=output_dataset.split('/')[0])
        # return FileResponse(archive_path, media_type="application/zip", filename=f"{dataset_name}.zip")
        return output_dataset

    except Exception as e:
        return HTTPException(status_code=404, detail=e.__str__())


# @router.get("/image/blurring/{dataset_name}/{degree}")
# def blacken_images_by_percentage(dataset_name: str, degree: float):
#     try:
#         dataset = dataset_service.load_dataset(dataset_name)
#         output_dataset = image_blurring_service.process_dataset(dataset, degree)

#         # archive_path = dataset_archive_service.create_archive(folder_to_compress=output_dataset, archive_name=output_dataset.split('/')[0])
#         # return FileResponse(archive_path, media_type="application/zip", filename=f"{dataset_name}.zip")
#         return output_dataset
#     except Exception as e:
#         return HTTPException(status_code=404, detail=e.__str__())


@router.get("/label/shuffle/{dataset_name}")
def shuffle_labels(dataset_name: str):
    try:
        dataset = dataset_service.load_dataset(dataset_name)
        output_dataset = label_flipping_service.process_dataset(dataset)

        # archive_path = dataset_archive_service.create_archive(folder_to_compress=output_dataset, archive_name=output_dataset.split('/')[0])
        # return FileResponse(archive_path, media_type="application/zip", filename=f"{dataset_name}.zip")
        return output_dataset

    except Exception as e:
        return HTTPException(status_code=404, detail=e.__str__())


@router.get("/shuffle/{dataset_name}")
def shuffle_images(dataset_name: str):
    try:
        dataset = dataset_service.load_dataset(dataset_name)
        output_dataset = image_shuffling_service.process_dataset(dataset)

        # archive_path = dataset_archive_service.create_archive(folder_to_compress=output_dataset, archive_name=output_dataset.split('/')[0])
        # return FileResponse(archive_path, media_type="application/zip", filename=f"{dataset_name}.zip")
        return output_dataset
    except Exception as e:
        return HTTPException(status_code=404, detail=e.__str__())


@router.get("/replace/{dataset_name}")
def replace_images(dataset_name: str):
    try:
        dataset = dataset_service.load_dataset(dataset_name)
        output_dataset = image_replacement_service.process_dataset(dataset)

        # archive_path = dataset_archive_service.create_archive(folder_to_compress=output_dataset, archive_name=output_dataset.split('/')[0])
        # return FileResponse(archive_path, media_type="application/zip", filename=f"{dataset_name}.zip")
        return output_dataset
    except Exception as e:
        return HTTPException(status_code=404, detail=e.__str__())
