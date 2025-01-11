from setuptools import setup, find_packages

setup(
    name="natural-query-lib",
    version="0.1.0",
    description="flexible SQL query builder written in Python! This library allows you to build and execute SQL queries with ease, while supporting dynamic parameters and JSON encoding for database compatibility.",
    author="Tu Nombre",
    author_email="tuemail@example.com",
    url="https://github.com/tuusuario/natural-query",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)