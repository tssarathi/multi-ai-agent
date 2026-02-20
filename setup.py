from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="multi-ai-agent",
    version="0.2",
    author="Sarathi",
    packages=find_packages(),
    install_requires=requirements,
)
