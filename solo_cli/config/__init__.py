import json
import os

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
