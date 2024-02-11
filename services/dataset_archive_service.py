import os
from zipfile import ZipFile


class DatasetArchiveService:
    def __init__(self):
        self.output_folder = "output/"
        self.output_archive_folder = "output/archives"

    def create_archive(self, folder_to_compress: str, archive_name: str) -> str:
        archive_name = archive_name + ".zip"

        archive_path = os.path.join(self.output_archive_folder, archive_name)
        folder_to_compress = os.path.join(self.output_folder, folder_to_compress)

        file_paths = []

        for root, directories, files in os.walk(folder_to_compress):
            for filename in files:
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)

        with ZipFile(archive_path, 'w') as zip:
            for f in file_paths:
                path = f.split("/")[2:]
                path = "/".join(path)
                zip.write(f, arcname=path)
        return archive_path
