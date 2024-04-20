from setuptools import find_packages,setup
from typing import List

HYPEN_E_DOT = '-e .'

def get_requirements(file_path:str) -> List[str]:
    """Get the requirements from the requirements.txt file.

    Args:
        file_path (str): the path to the requirements.txt file

    Returns:
        List[str]: list of requirements
    """
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    
    return requirements

setup(
    name='food-label-scanner',
    version='0.0.1',
    author='Ishan Srivastava',
    author_email='ishan.alld@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)