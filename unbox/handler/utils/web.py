import requests
import os

def download_file(url, destination):
    local_filename = os.path.join(destination, url.split('/')[-1])
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    if not os.path.exists(destination):
        os.mkdir(destination)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename