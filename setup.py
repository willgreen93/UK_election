from setuptools import setup, find_packages

with open("requirements.txt") as f:
    lines = f.readlines()
libs = [line.strip() for line in lines]

setup(name="uk_election", packages=find_packages(), install_requires=libs)
