from setuptools import setup, find_packages

setup(
    name="manoon_crew",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "crewai",
        "langchain-community",
        "python-dotenv",
        "pyyaml"
    ],
) 