from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='estela_requests',
    version='0.0.1-a1',
    description='estela_requests is a request wrapper for estela.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bitmakerla/estela-requests",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "estela>=0.0.2",
        "requests>=2.0.0",
    ],
)
