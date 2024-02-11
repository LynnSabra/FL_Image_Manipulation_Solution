import os
import shutil
import sys
from PIL import Image
import datetime

original_dataset = sys.argv[1]

## we can use this for loop to blacken all the images inside the dataset
for folder_name in os.listdir(original_dataset):
    for image_path in os.listdir(original_dataset + folder_name):
        image = Image.open(original_dataset + folder_name + "/" + image_path)
        h, w = image.size
        black = Image.new(str(image.mode), (h, w), 'black')
        result = Image.blend(image, black, 1)
        image.paste(result)
        image.save(original_dataset + folder_name + "/" + image_path)  


n = len (os.listdir(original_dataset))
black_image = Image.new("RGB", (100, 100), 'black')

## OR we can insert black images inside the dataset
for i in range (int(0.5*n)):
    for folder_name in os.listdir(original_dataset):
        black_image.save(original_dataset + folder_name + "/" + str(datetime.datetime.now()) + ".jpg")
