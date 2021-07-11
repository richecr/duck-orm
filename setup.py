import os
import re
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    with open(os.path.join(package, "__init__.py")) as f:
        return re.search("__version__ = ['\"]([^'\"]+)['\"]", f.read()).group(1)


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [
        dirpath
        for dirpath, dirnames, filenames in os.walk(package)
        if os.path.exists(os.path.join(dirpath, "__init__.py"))
    ]


keywords = "orm async aiohttp asyncio databases database postgres sqlite"

setup(
    name="duck-orm",
    version="0.1.0",
    author="Rich Carvalho",
    python_requires=">=3.8",
    author_email="richelton14@gmail.com",
    description="DuckORM is package is an asynchronous ORM for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=get_packages("duck_orm"),
    install_requires=[
        "databases" >= "0.4.3",
        "sqlalchemy" >= "1.3.24",
    ],
    extras_require={
        "postgresql": ["asyncpg"],
        "postgresql+aiopg": ["aiopg"],
        "sqlite": ["aiosqlite"]
    },
    include_package_data=True,
    url="https://github.com/richecr/duck-orm",
    project_urls={
        "Código fonte": "https://github.com/richecr/duck-orm",
    },
    keywords=keywords,
    license="MIT"
)
