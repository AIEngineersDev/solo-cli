# Solo CLI

A CLI tool to manage and execute LLaMA files.

## 🌟 Features

- Initialize and download models
- Pull specific models by name
- Quickstart to execute a default model
- Serve models on the internet using ngrok
- Start models with specific configurations

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- Pip (Python package installer)
- ngrok account (optional, for serving models)

### Installation

Install the package using pip:

```bash
pip install solo-cli
```

### Usage

```bash
solo-cli init
solo-cli pull model_name
solo-cli quickstart
solo-cli serve --port 8080
solo-cli start model_name --port 8080
```

## 📖 Examples

### Initialize
```bash
solo-cli init
```
### Pull a Model
```bash
solo-cli pull llava-v1.5-7b-q4
```
### Quickstart
```bash
solo-cli quickstart
```
### Serve a Model
```bash
solo-cli serve --port 8080
```
### Start a Model
```bash
solo-cli start llava-v1.5-7b-q4 --port 8080
```

## 📦 Dependencies
Typer
Requests
tqdm
ngrok

## 🗺️ Roadmap
Add support for more models
Improve error handling
Add more configuration options

## 🤝 Contribution
Contributions are welcome! Please open an issue or submit a pull request on GitHub.