import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="json_parser",
    version="0.1.0",
    author="Tushar Sadhwani",
    author_email="tushar.sadhwani000@gmail.com",
    description="A JSON parser written in Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tusharsadhwani/json_parser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['pytest'],
)
