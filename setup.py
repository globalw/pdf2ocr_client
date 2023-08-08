from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pdf2ocr_client",
    version="0.1",
    author="Wilhelm Bender",
    author_email="",
    description="Convert pdf to pdf with text-layer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com:globalw/pdf2ocr_client.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
