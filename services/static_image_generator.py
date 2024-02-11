import os
import shutil
import asyncio
import aiohttp

import requests

URL = "https://picsum.photos/"


async def get(session: aiohttp.ClientSession, image_path, width, height):
    url = URL + str(width) + "/" + str(height)
    print(f"Requesting {url}")
    resp = await session.request('GET', url=url)

    # Note that this may raise an exception for non-2xx responses
    # You can either handle that here, or pass the exception through
    data = await resp.content.read()
    with open(f'{image_path}.png', 'wb') as out_file:
        out_file.write(data)
    print("Done downloading image")
    del data
    return "sss"


async def main():
    output_path = os.path.join("images")
    # Asynchronous context manager.  Prefer this rather
    # than using a different session for each GET request
    async with aiohttp.ClientSession(auto_decompress=False) as session:
        tasks = []
        for i in range(900):
            image_name = os.path.join(output_path, str(i))
            tasks.append(get(session=session, image_path=image_name, width=600, height=500))
        # asyncio.gather() will wait on the entire task set to be
        # completed.  If you want to process results greedily as they come in,
        # loop over asyncio.as_completed()
        htmls = await asyncio.gather(*tasks, return_exceptions=True)
    print(htmls)
    return htmls


# def generate_static_image(image_path, width, height):
#     url = URL + str(width) + "/" + str(height)
#     # sent get requests to the url and save the response as image
#     response = requests.get(url, stream=True)
#
#     with open(f'{image_name}.png', 'wb') as out_file:
#         shutil.copyfileobj(response.raw, out_file)
#     print("Done downloading image")
#     del response

#
if __name__ == '__main__':
    asyncio.run(main())
