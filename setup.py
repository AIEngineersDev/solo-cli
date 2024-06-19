from setuptools import setup, find_packages

setup(
    name="solo-cli",
    version="0.2.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "typer",
        "GPUtil",
        "psutil",
        "tqdm",
        "requests"
    ],
    entry_points={
        "console_scripts": [
            "solo-cli = solo_cli.main:app",
        ],
    },
    author="Dhruv Diddi",
    author_email="dhruv.diddi@gmail.com",
    description="A CLI tool to manage and recommend machine learning models based on system GPU and memory.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AIEngineersDev/solo-cli",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
