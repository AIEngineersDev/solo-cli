import typer
from solo_cli.utils import download_file, set_permissions
import subprocess

app = typer.Typer()

@app.command()
def init():
    url = 'https://huggingface.co/Mozilla/llava-v1.5-7b-llamafile/resolve/main/llava-v1.5-7b-q4.llamafile?download=true'
    filename = 'llava-v1.5-7b-q4.llamafile'
    
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

if __name__ == "__main__":
    app()
