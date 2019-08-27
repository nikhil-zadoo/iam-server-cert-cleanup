from setuptools import setup

setup(
    name="datadog_atlas",
    version="1.0",
    install_requires=[
        'boto3',
        'logging',
        'datetime'
    ]
)