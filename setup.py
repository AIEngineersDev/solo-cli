from setuptools import setup, find_packages

setup(
    name="solo-cli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "typer",
        "requests",
        "tqdm"
    ],
    entry_points={
        'console_scripts': [
            'solo-cli=solo_cli.main:app',
        ],
    },
)
