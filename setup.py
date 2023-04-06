from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="digitinterface",
    version="0.1.0",
    author="Alphonsus Adu-Bredu",
    author_email="adubredu@umich.edu",
    description="Python package for interacting with the Agility Robotics Digit v3 default controller interface.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adubredu/digitinterface", 
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires='>=3.6',
    install_requires=[
        # Add your package's dependencies here, e.g.,
        "numpy>=1.18.0",
        "ws4py", 
    ],
)