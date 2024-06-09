import os
import platform
import requests
import subprocess
from tqdm import tqdm

def download_file(url, filename):
    if os.path.exists(filename):
        print(f"{filename} already exists. Skipping download.")
        return
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte
    t = tqdm(total=total_size, unit='iB', unit_scale=True)
    with open(filename, 'wb') as file:
        for data in response.iter_content(block_size):
            t.update(len(data))
            file.write(data)
    t.close()
    if total_size != 0 and t.n != total_size:
        print("ERROR: Something went wrong")
    else:
        print(f"{filename} downloaded successfully.")

def set_permissions(filename):
    if platform.system() in ['Linux', 'Darwin', 'BSD']:
        subprocess.run(['chmod', '+x', filename], check=True)
    elif platform.system() == 'Windows':
        new_filename = f"{filename}.exe"
        os.rename(filename, new_filename)
        return new_filename
    return filename
