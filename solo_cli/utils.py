import os
import platform
import requests
import subprocess
from tqdm import tqdm
import GPUtil
import psutil

# Model data
models = [
    {"name": "LLaVA 1.5", "memory": 3.97, "license": "LLaMA 2", "file": "llava-v1.5-7b-q4.llamafile"},
    {"name": "TinyLlama-1.1B", "memory": 2.05, "license": "Apache 2.0", "file": "TinyLlama-1.1B-Chat-v1.0.F16.llamafile"},
    {"name": "Mistral-7B-Instruct", "memory": 3.85, "license": "Apache 2.0", "file": "mistral-7b-instruct-v0.2.Q4_0.llamafile"},
    {"name": "Phi-3-mini-4k-instruct", "memory": 7.67, "license": "Apache 2.0", "file": "Phi-3-mini-4k-instruct.F16.llamafile"},
    {"name": "Mixtral-8x7B-Instruct", "memory": 30.03, "license": "Apache 2.0", "file": "mixtral-8x7b-instruct-v0.1.Q5_K_M.llamafile"},
    {"name": "WizardCoder-Python-34B", "memory": 22.23, "license": "LLaMA 2", "file": "wizardcoder-python-34b-v1.0.Q5_K_M.llamafile"},
    {"name": "WizardCoder-Python-13B", "memory": 7.33, "license": "LLaMA 2", "file": "wizardcoder-python-13b.llamafile"}
]

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

def get_system_gpu_memory():
    gpus = GPUtil.getGPUs()
    if not gpus:
        return 0
    return max(gpu.memoryTotal for gpu in gpus)

def get_system_memory():
    return psutil.virtual_memory().total / (1024 ** 3)  # Convert bytes to GB

def recommend_model(gpu_memory, system_memory):
    recommended_models = [model for model in models if model["memory"] <= gpu_memory and model["memory"] <= system_memory]
    if not recommended_models:
        return "No models can be supported with the current system configuration."
    
    recommended_models.sort(key=lambda x: x["memory"])
    return recommended_models
