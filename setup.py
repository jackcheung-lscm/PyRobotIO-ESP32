from setuptools import setup, find_packages

setup(
    name='robot_sensor',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pyserial',
        'fastapi',
        'uvicorn',
        'aiohttp',
        'aiofiles',
        'pydantic',
        'aiohttp-cors'
    ],
)