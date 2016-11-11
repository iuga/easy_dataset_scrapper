from setuptools import setup, find_packages

setup(
    name="easy dataset scrapper",
    version="0.1-beta",
    description="A lightweight base class to create a dataset scrapper",
    author="Iuga",
    packages=find_packages(exclude=["tests", "tools", "docs", ".github"]),
    install_requires=[]
)
