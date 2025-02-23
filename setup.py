from setuptools import setup, find_packages
from typing import List



def get_requirements()->List[str]:
    """
    This function will return list of requirements
    """

    requirements_lst:List[str]=[]
    try:
        with open('requirements.txt','r') as file:
            # Read lines from the files
            lines=file.readlines()
            for line in lines:
                requirement=line.strip()
                if requirement and requirement!= '-e .':
                    requirements_lst.append(requirement)
    except FileNotFoundError:
        print("requirement.txt file not found")

    return requirements_lst


setup(
    name='ai_analayst',
    version='0.0.0',
    author='Sameer',
    author_email='Sameerup199@gmail.com',
    packages=find_packages()
)