import os
import platform
import requests
import typer
from pathlib import Path
from tqdm import tqdm

app = typer.Typer()

DOWNLOAD_URL = "https://huggingface.co/Mozilla/llava-v1.5-7b-llamafile/resolve/main/llava-v1.5-7b-q4.llamafile?download=true"
FILENAME = "llava-v1.5-7b-q4.llamafile"

def download_file(url: str, dest: Path):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))
    block_size = 8192
    t = tqdm(total=total_size, unit='iB', unit_scale=True)
    
    with open(dest, "wb") as f:
        for chunk in response.iter_content(chunk_size=block_size):
            if chunk:
                f.write(chunk)
                t.update(len(chunk))
    t.close()

    if total_size != 0 and t.n != total_size:
        typer.echo("ERROR: Something went wrong during the download.")

@app.command()
def download():
    dest_path = Path(FILENAME)

    typer.echo(f"Downloading {FILENAME} from {DOWNLOAD_URL}...")
    download_file(DOWNLOAD_URL, dest_path)
    typer.echo(f"Downloaded {FILENAME} to {dest_path}")

    if platform.system() in ["Linux", "Darwin"]:  # macOS and Linux
        typer.echo("Granting execute permissions for the downloaded file...")
        os.chmod(dest_path, 0o755)
        typer.echo("Permissions granted.")
    elif platform.system() == "Windows":
        exe_path = dest_path.with_suffix(".exe")
        dest_path.rename(exe_path)
        typer.echo(f"Renamed the file to {exe_path}")

    typer.echo("You can now run the llamafile with the following command:")
    if platform.system() in ["Linux", "Darwin"]:
        typer.echo(f"./{dest_path.name}")
    elif platform.system() == "Windows":
        typer.echo(f"{exe_path.name}")

if __name__ == "__main__":
    app()
