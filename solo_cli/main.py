import typer
from solo_cli.utils import download_file, set_permissions, get_system_gpu_memory, get_system_memory, recommend_model
import subprocess

app = typer.Typer()

@app.command()
def init():
    gpu_memory = get_system_gpu_memory()
    system_memory = get_system_memory()
    
    typer.echo(f"System GPU Memory: {gpu_memory:.2f} GB")
    typer.echo(f"System Memory: {system_memory:.2f} GB")
    
    recommended_models = recommend_model(gpu_memory, system_memory)
    if isinstance(recommended_models, str):
        typer.echo(recommended_models)
    else:
        best_model = recommended_models[0]
        url = f"https://huggingface.co/Mozilla/{best_model['file']}?download=true"
        filename = best_model['file']
        
        download_file(url, filename)
        set_permissions(filename)
        typer.echo(f"Model {best_model['name']} downloaded and permissions set.")

@app.command()
def pull(url: str):
    filename = url.split('/')[-1]
    download_file(url, filename)
    set_permissions(filename)

@app.command()
def quickstart():
    llamafile = 'llava-v1.5-7b-q4.llamafile'
    shell_script = f"{llamafile}.sh"

    with open(shell_script, 'w') as f:
        f.write(f"#!/bin/bash\n./{llamafile}")

    set_permissions(shell_script)

    subprocess.run(['./' + shell_script], check=True)

@app.command()
def start(model: str, port_number: int):
    shell_script = f"{model}.sh"

    with open(shell_script, 'w') as f:
        f.write(f"#!/bin/bash\n./{model} --port {port_number}")

    set_permissions(shell_script)

    subprocess.run(['./' + shell_script], check=True)

@app.command()
def serve(port_number: int):
    # Ensure you have ngrok installed and authenticated with your account
    subprocess.run(['ngrok', 'http', str(port_number)], check=True)

if __name__ == "__main__":
    app()
