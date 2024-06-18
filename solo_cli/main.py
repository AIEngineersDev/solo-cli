import typer
import subprocess
import requests

from solo_cli.utils import download_file, set_permissions, start_ngrok_service, start_model,\
    check_node_installed, install_node, clone_repo, run_npm_install, run_docker_mongodb, prompt_huggingface_token,\
    create_env_file, load_config, update_config, run_solo_chat_ui
from solo_cli.constants import API_BASE_URL, models, DEFAULT_MODEL

app = typer.Typer()

@app.command()
def list_models():
    """
    List available models from the Hugging Face repository.
    """
    response = requests.get(API_BASE_URL)
    if response.status_code == 200:
        models = response.json()
        typer.echo("Available Models:")
        for model in models:
            typer.echo(f"- {model['modelId']}")
    else:
        typer.echo("Failed to fetch models", err=True)

@app.command()
def init():
    url = models[DEFAULT_MODEL]
    filename = f"{DEFAULT_MODEL}.llamafile"

    download_file(url, filename)
    set_permissions(filename)
    update_config('model_name', DEFAULT_MODEL)


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
    config = load_config()
    llamafile = f"{config.get('model_name', DEFAULT_MODEL)}.llamafile"
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

        update_config('model_name', model_name)

        with open(shell_script, 'w') as f:
            f.write(f"#!/bin/bash\n./{filename}")

        set_permissions(shell_script)

        subprocess.run(['./' + shell_script], check=True)
    else:
        print(f"Model {model_name} not found. Please provide a valid model name.")


@app.command()
def initapp():
    if not check_node_installed():
        install_node()
    else:
        print("Node.js is already installed.")

    clone_repo()
    run_npm_install()
    run_docker_mongodb()

    # Prompt the user for Hugging Face token
    prompt_huggingface_token()
    init()
    create_env_file()
    run_solo_chat_ui()


if __name__ == "__main__":
    app()
