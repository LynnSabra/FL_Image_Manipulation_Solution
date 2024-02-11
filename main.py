import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.controllers import dataset_controller,image_manipulation_controller

app = FastAPI(version="1.0", title="Image Replacement API", description="API for image replacement used in Federated learning")

# app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dataset_controller.router, prefix="/api/dataset", tags=["dataset"])
app.include_router(image_manipulation_controller.router, prefix="/api/image/manipulation", tags=["image"])

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=6900)
