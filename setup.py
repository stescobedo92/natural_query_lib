from setuptools import setup, find_packages

setup(
    name="natural_query_lib",
    version="0.1.1",
    description="flexible SQL query builder written in Python! This library allows you to build and execute SQL queries with ease, while supporting dynamic parameters and JSON encoding for database compatibility.",
    author="Sergio Triana Escobedo",
    author_email="stescobedo.31@gmail.com",
    url="https://github.com/stescobedo92/natural_query_lib",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)