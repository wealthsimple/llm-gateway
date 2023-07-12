import os
from os.path import exists

from setuptools import find_packages, setup

description = open("README.md").read() if exists("README.md") else ""

setup(
    name="llm_gateway",
    description="",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/wealthsimple/llm-gateway",
    author="Wealthsimple Data Science & Engineering",
    author_email="data@wealthsimple.com",
    license="Apache License 2.0",
    packages=find_packages(include=["llm_gateway", "front_end"]),
    package_data={"front_end": ["front_end/**"]},
    entry_points={
        "console_scripts": [
            "llm_gateway = llm_gateway.cli:cli",
        ],
    },
    use_scm_version={
        "write_to": "llm_gateway/_version.py",
        "fallback_version": "0.0.0",
        "local_scheme": "no-local-version",
    },
    setup_requires=["setuptools_scm"],
    install_requires=[
        "click",
        "fastapi>=0.95.0",
        "pydantic>=1.10.7",
        "psycopg2-binary~=2.9.3",
        "alembic~=1.8.0",
        "sqlalchemy>=1.3.0",
        "uvicorn[standard]>=0.21.1",
        "openai[datalib]>=0.27.4",
        "cohere>=4.6.1",
        "click>=8.1.4",
    ],
    extras_require={
        "openai": [
            "datalib",
        ],
        "dev": [
            "black==23.3.0",
            "isort==5.12.0",
            "flake8>=6.0.0",
            "pre-commit>=3.2.2",
            "pytest>=7.3.0",
            "urllib3==1.26.15",
        ],
    },
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
