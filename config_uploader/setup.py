#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="study_area_uploader",
    packages=find_packages(),
    install_requires=["google-cloud-storage", "Jinja2"],
    entry_points={
        "console_scripts": [
            "upload_citycat_config = config_uploader.main:main",
        ],
    },
    extras_require={
        "dev": [
            "black~=24.0",
            "flake8~=7.0",
            "flake8-docstrings~=1.7",
            "pytest~=8.0",
            "mypy~=1.9",
        ]
    },
)
