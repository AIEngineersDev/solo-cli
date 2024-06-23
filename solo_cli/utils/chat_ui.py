import os
import platform
import subprocess

from solo_cli.config import load_config, update_config

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
    try:
        # Kill the previous process if running
        print("Checking for running processes...")
        result = subprocess.run(['pgrep', '-f', 'solo-chat-ui/node_modules/.bin/vite'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        if result.returncode == 0:
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                print(f"Killing process with PID {pid}")
                subprocess.run(['kill', '-9', pid],stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

    except subprocess.CalledProcessError as e:
        print(e)

    root_path = load_config().get('dir', './')
    dir_path = os.path.join(root_path, repo_dir)
    print(f"Running `npm run dev` on {dir_path}...")
    subprocess.run(['npm', 'run', 'dev'], cwd=dir_path, check=True)

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
        # Check if the container is already running
        result = subprocess.run(['docker', 'inspect', '--format', '{{.State.Running}}', 'mongo-chatui'], capture_output=True, text=True, check=True)
        if result.stdout.strip() == 'true':
            print("MongoDB Docker container is already running.")
        else:
            print("MongoDB Docker container is not running. Starting it...")
            subprocess.run(['docker', 'start', 'mongo-chatui'], check=True)

    except subprocess.CalledProcessError as e:
        # If the container doesn't exist, create and run it
        print("MongoDB Docker container not found. Creating and starting it...")
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

