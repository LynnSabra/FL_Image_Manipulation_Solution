import requests


class PicSumImageClient:

    def __init__(self):
        self.URL = "https://picsum.photos"

    def get_image(self, width: int = 600, height: int = 600) -> bytes:
        url = self.URL + "/" + str(width) + "/" + str(height)
        print(f"Requesting {url}", flush=True)
        response = requests.get(url, stream=True)
        print("Done downloading image", flush=True)
        return response.raw
