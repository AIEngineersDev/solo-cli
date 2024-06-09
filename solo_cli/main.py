import typer
from solo_cli.utils import download_file, set_permissions, start_ngrok_service, start_model
import subprocess

app = typer.Typer()

models = {
    "llava-v1.5-7b-q4": "https://huggingface.co/Mozilla/llava-v1.5-7b-llamafile/resolve/main/llava-v1.5-7b-q4.llamafile?download=true",
    "TinyLlama-1.1B-Chat-v1.0.F16": "https://huggingface.co/somepath/TinyLlama-1.1B-Chat-v1.0.F16.llamafile?download=true",
    "mistral-7b-instruct-v0.2.Q4_0": "https://huggingface.co/somepath/mistral-7b-instruct-v0.2.Q4_0.llamafile?download=true",
    "Phi-3-mini-4k-instruct.F16": "https://huggingface.co/somepath/Phi-3-mini-4k-instruct.F16.llamafile?download=true",
    "mixtral-8x7b-instruct-v0.1.Q5_K_M": "https://huggingface.co/somepath/mixtral-8x7b-instruct-v0.1.Q5_K_M.llamafile?download=true",
    "wizardcoder-python-34b-v1.0.Q5_K_M": "https://huggingface.co/somepath/wizardcoder-python-34b-v1.0.Q5_K_M.llamafile?download=true",
    "wizardcoder-python-13b": "https://huggingface.co/somepath/wizardcoder-python-13b.llamafile?download=true",
    "Meta-Llama-3-70B-Instruct.Q4_0": "https://huggingface.co/somepath/Meta-Llama-3-70B-Instruct.Q4_0.llamafile?download=true",
    "Meta-Llama-3-8B-Instruct.Q5_K_M": "https://huggingface.co/somepath/Meta-Llama-3-8B-Instruct.Q5_K_M.llamafile?download=true",
    "rocket-3b.Q5_K_M": "https://huggingface.co/somepath/rocket-3b.Q5_K_M.llamafile?download=true",
    "e5-mistral-7b-instruct-Q5_K_M": "https://huggingface.co/somepath/e5-mistral-7b-instruct-Q5_K_M.llamafile?download=true",
    "mxbai-embed-large-v1-f16": "https://huggingface.co/somepath/mxbai-embed-large-v1-f16.llamafile?download=true"
}

@app.command()
def init():
    url = models["llava-v1.5-7b-q4"]
    filename = 'llava-v1.5-7b-q4.llamafile'
    
    download_file(url, filename)
    set_permissions(filename)

@app.command()
def pull(model_name: str):
    if model_name in models:
        url = models[model_name]
        filename = f"{model_name}.llamafile"
        download_file(url, filename)
        set_permissions(filename)
    else:
        print(f"Model {model_name} not found. Please provide a valid model name.")

@app.command()
def quickstart():
    llamafile = 'llava-v1.5-7b-q4.llamafile'
    shell_script = f"{llamafile}.sh"

    with open(shell_script, 'w') as f:
        f.write(f"#!/bin/bash\n./{llamafile}")

    set_permissions(shell_script)

    subprocess.run(['./' + shell_script], check=True)

@app.command()
def serve(port: int = 8080):
    start_ngrok_service(port)

@app.command()
def start(model_name: str, port: int):
    if model_name in models:
        filename = f"{model_name}.llamafile"
        shell_script = f"{filename}.sh"
        
        with open(shell_script, 'w') as f:
            f.write(f"#!/bin/bash\n./{filename}")

        set_permissions(shell_script)
        
        subprocess.run(['./' + shell_script], check=True)
    else:
        print(f"Model {model_name} not found. Please provide a valid model name.")

if __name__ == "__main__":
    app()
