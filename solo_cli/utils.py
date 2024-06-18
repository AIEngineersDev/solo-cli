import json
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

def start_ngrok_service(port):
    system = platform.system()
    config_path = "path/to/config.yml"

    if system == "Linux":
        if os.path.exists("/etc/systemd/system/"):
            with open("/etc/systemd/system/ngrok.service", "w") as service_file:
                service_file.write(
                    f"""
                    [Unit]
                    Description=Ngrok
                    After=network.service

                    [Service]
                    Type=simple
                    User={os.getenv("USER")}
                    WorkingDirectory={os.getenv("HOME")}
                    ExecStart=/usr/bin/ngrok start --all --config="{config_path}"
                    Restart=on-failure

                    [Install]
                    WantedBy=multi-user.target
                    """
                )
            subprocess.run(["systemctl", "enable", "ngrok.service"], check=True)
            subprocess.run(["systemctl", "start", "ngrok.service"], check=True)
        else:
            subprocess.run(["nohup", "ngrok", "start", "--all", "--config", config_path, f"--port={port}", "&"], check=True)
    elif system == "Darwin":
        subprocess.run(["nohup", "ngrok", "start", "--all", "--config", config_path, f"--port={port}", "&"], check=True)
    elif system == "Windows":
        subprocess.run(["nssm", "install", "ngrok", "ngrok", "start", "--all", "--config", config_path, f"--port={port}"], check=True)
        subprocess.run(["sc", "start", "ngrok"], check=True)
    else:
        print(f"Unsupported operating system: {system}")

    print(f"Ngrok service started. Port {port} is available on the internet.")

def start_model():
    # Placeholder for start model functionality
    print("Starting model...")

def check_node_installed():
    """
        Check if Node.js is installed.
    """
    try:
        result = subprocess.run(['node', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print(f"Node.js is installed: {result.stdout.decode().strip()}")
            return True
        else:
            print("Node.js is not installed.")
            return False
    except FileNotFoundError:
        print("Node.js is not installed.")
        return False

def install_node():
    """
        Install Node.js based on the operating system.
    """
    os_type = platform.system()

    if os_type == "Linux":
        print("Installing Node.js for Linux...")
        subprocess.run(['sudo', 'apt-get', 'update'])
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 'nodejs'])
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 'npm'])
    elif os_type == "Darwin":  # macOS
        print("Installing Node.js for macOS...")
        subprocess.run(['/bin/bash', '-c', '$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)'])
        subprocess.run(['brew', 'install', 'node'])
    elif os_type == "Windows":
        print("Please install Node.js manually from https://nodejs.org/")
    else:
        print(f"Unsupported OS: {os_type}")


def clone_repo():
    """
        Clone the specified repository.
    """
    repo_url = "https://github.com/AIEngineersDev/solo-chat-ui.git"
    repo_dir = "solo-chat-ui"

    if not os.path.exists(repo_dir):
        print(f"Cloning repository from {repo_url}...")
        subprocess.run(['git', 'clone', repo_url])
    else:
        print(f"Repository {repo_dir} already exists.")


def run_npm_install(repo_dir="solo-chat-ui"):
    """
        Run npm install in the specified directory.
    """
    print(f"Running npm install in {repo_dir}...")
    subprocess.run(['npm', 'install'], cwd=repo_dir)


def run_solo_chat_ui(repo_dir="solo-chat-ui"):
    """
        Run npm dev in the solo chat ui directory.
    """
    # Run npm run dev in the cloned repository
    print(f"Running `npm run dev` on {repo_dir}...")
    try:
        subprocess.run(['npm', 'run', 'dev'], cwd=repo_dir, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Running `npm run dev` on {repo_dir}, error: {e}")


def start_docker_daemon():
    import time

    """Start the Docker daemon if it's not running."""
    try:
        subprocess.run(['docker', 'info'], check=True)
        print("Docker daemon is already running.")
    except subprocess.CalledProcessError:
        print("Docker daemon is not running. Starting it now...")
        subprocess.run(['open', '--background', '-a', 'Docker'])
        time.sleep(5)  # Wait for 5 seconds for Docker to start
        print("Docker daemon started successfully.")

def run_docker_mongodb(repo_dir="solo-chat-ui"):
    """
    Run MongoDB Docker container.
    """
    start_docker_daemon()
    print("Starting MongoDB Docker container...")
    try:
        subprocess.run(['docker', 'run', '-d', '-p', '27017:27017', '--name', 'mongo-chatui', 'mongo:latest'], cwd=repo_dir, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to run MongoDB Docker container: {e}")


def prompt_huggingface_token():
    """Prompt the user to enter their Hugging Face token if not already present."""
    config = load_config()
    if 'HF_TOKEN' in config:
        print("Checking for Hugging Face token... Token already present.")
        return

    print("Please open the following URL and create a token:")
    print("https://huggingface.co/settings/token")
    token = input("Enter your Hugging Face token: ")
    update_config('HF_TOKEN', token)
    print("Hugging Face token saved in configuration.")



def create_env_file(repo_dir="solo-chat-ui"):
    """
        Create .env file with HF_TOKEN, MODEL_NAME, and MODEL in the cloned repository.
    """
    print("Creating ENV file")
    config = load_config()
    hf_token = config.get('HF_TOKEN', '')
    # model_name = config.get('model_name', '')

    model_variable = """
MODELS=`[
    {
        "name": "Local liuhaotian/llava-v1.5-7b",
        "displayName": "liuhaotian/llava-v1.5-7b",
        "description": "The primary intended users of the model are researchers and hobbyists in computer vision, natural language processing, machine learning, and artificial intelligence.",
        "websiteUrl": "https://llava-vl.github.io/",
        "preprompt": "",
      "chatPromptTemplate" : "<s>{{#each messages}}{{#ifUser}}[INST] {{#if @first}}{{#if @root.preprompt}}{{@root.preprompt}}\\n{{/if}}{{/if}}{{content}} [/INST]{{/ifUser}}{{#ifAssistant}}{{content}}</s>{{/ifAssistant}}{{/each}}",
      "parameters": {
        "temperature": 0.1,
        "top_p": 0.95,
        "repetition_penalty": 1.2,
        "top_k": 50,
        "truncate": 3072,
        "max_new_tokens": 1024,
        "stop": ["</s>"]
      },
      "promptExamples": [
        {
          "title": "Write an email from bullet list",
          "prompt": "As a restaurant owner, write a professional email to the supplier to get these products every week: \\n\\n- Wine (x10)\\n- Eggs (x24)\\n- Bread (x12)"
        }, {
          "title": "Code a snake game",
          "prompt": "Code a basic snake game in python, give explanations for each step."
        }, {
          "title": "Assist in a task",
          "prompt": "How do I make a delicious lemon cheesecake?"
        }
      ],
        "endpoints": [{
            "type" : "llamacpp",
            "baseURL": "http://localhost:8080"
        }],
    }
]`
"""

    MONGODB_VAR = "MONGODB_URL=mongodb://localhost:27017"

    env_content = f"HF_TOKEN={hf_token}\n{model_variable}\n{MONGODB_VAR}"

    env_file_path = os.path.join(repo_dir, '.env.local')
    with open(env_file_path, 'w') as env_file:
        env_file.write(env_content)

    print("Created ENV successfully!")



# Define the config file path
CONFIG_DIR = "config"
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

# Ensure the config directory exists
os.makedirs(CONFIG_DIR, exist_ok=True)

def load_config():
    """Load the configuration file."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            return json.load(file)
    else:
        return {}

def save_config(config):
    """Save the configuration file."""
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file, indent=4)

def update_config(key, value):
    """Update a specific configuration value."""
    config = load_config()
    config[key] = value
    save_config(config)
