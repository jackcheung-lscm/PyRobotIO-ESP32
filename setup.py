import io
import os
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="PyRobotIO-ESP32",
    version="0.0.1",
    packages=find_packages(exclude=["tests", ".github"]),
    description="PyRobotIO-ESP32 created by jackcheung-lscm",
    author="jackcheung-lscm",
    author_email="jcheung@lscm.hk",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/jackcheung-lscm/PyRobotIO-ESP32/",
    install_requires=read_requirements("requirements.txt"),
    extras_require={
        "dev": read_requirements("requirements-test.txt")
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    package_data={
        '': ['*'],  # "PeopleCounting": ["models/head_detector.pt"]
    },
)