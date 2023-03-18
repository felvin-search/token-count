from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="token-count",
    version="0.1.4",
    packages=find_packages(),
    install_requires=[
        "tiktoken",
        "gitignore-parser",
    ],
    entry_points={
        "console_scripts": [
            "token-count = token_count:main",
        ],
    },
    author="Felvin",
    author_email="team@felvin.com",
    description="Count the number of tokens in a text string or file, similar to the Unix 'wc' utility.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/felvin-search/token-count",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)