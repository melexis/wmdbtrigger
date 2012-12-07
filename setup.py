from setuptools import setup, find_packages

setup(
    name='wmdbtrigger',
    description='python library that sends events when a new wafermap is saved in the wmdb',
    version='1.0.0',
    long_description=__doc__,
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    zip_safe=False,
    install_requires=[]
)
