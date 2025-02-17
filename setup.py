'''
The setup.py file is an essential part of packaging & distributing python packages. It contains the metadata and instructions for building the package. It is used by setuptools to define the configuration of our project, like metadata, dependencies, etc.
'''

from setuptools import find_packages, setup
from typing import List

def get_requirements() -> List[str]:
    """
    this function will return list of requirements
    """
    requirement_lst : List[str] = []
    try:
        with open('requirements.txt', 'r') as file:
            # Read lines from requirements.txt
            lines = file.readlines()
            # Process Each Line
            for line in lines:
                requirement = line.strip()
                # ignore empty lines & -e .
                if requirement and requirement != '-e .':
                    requirement_lst.append(requirement)
        
    except FileNotFoundError:
        print("requirements.txt file Not found")

    return requirement_lst

# Checking ki whether it is working fine or not
# print(get_requirements())

# setup the metadata
setup(
    name="AI-Powered Network Security : Phising Detection",
    version="0.0.1",
    author="Chirag Verma",
    author_email="chirag.yep@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)
