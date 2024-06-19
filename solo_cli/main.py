import typer
import subprocess
import requests
import concurrent.futures

from solo_cli.utils.llama_server import download_file, set_permissions, start_ngrok_service, start_model
from solo_cli.constants import API_BASE_URL, MODELS, DEFAULT_MODEL
from solo_cli.config import load_config, update_config
from solo_cli.utils.chat_ui import check_node_installed, install_node, clone_repo, run_npm_install,\
    run_docker_mongodb, prompt_huggingface_token, create_env_file, run_solo_chat_ui

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
    url = MODELS[DEFAULT_MODEL]
    filename = f"{DEFAULT_MODEL}.llamafile"

    download_file(url, filename)
    set_permissions(filename)
    update_config('model_name', DEFAULT_MODEL)


@app.command()
def pull(model_name: str):
    if model_name in MODELS:
        url = MODELS[model_name]
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
        f.write(f"#!/bin/bash\n./{llamafile} --nobrowser")

    set_permissions(shell_script)

    subprocess.run(['./' + shell_script], check=True)

@app.command()
def serve(port: int = 8080):
    start_ngrok_service(port)

@app.command()
def start(model_name: str, port: int):
    if model_name in MODELS:
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

    # get selected model
    config = load_config()
    # incase no model selected initiate default model download
    if not config.get('model_name'):
        init()

    # create env file for chat ui
    create_env_file()

    # Run solo_chat_ui and model server start in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_run_solo_chat_ui = executor.submit(run_solo_chat_ui)
        future_quickstart = executor.submit(quickstart)

        # Wait for both to complete
        concurrent.futures.wait([future_run_solo_chat_ui, future_quickstart])

    print("Both servers have been started.")


if __name__ == "__main__":
    app()
