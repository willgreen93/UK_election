from setuptools import setup, find_packages

with open("requirements.txt") as f:
    lines = f.readlines()
libs = [line.strip() for line in lines]

setup(name="interface", packages=find_packages(), install_requires=libs)
