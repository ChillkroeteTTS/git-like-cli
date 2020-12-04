import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="git-like", # Replace with your own username
    version="0.0.6",
    author="Tjark Smalla",
    scripts=['gitlike/git-like'],
    author_email="tjark.smalla@git-like.com",
    description="A small cli to like and receive likes four your code in a git controlled code base.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ChillkroeteTTS/git-like-cli",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'click',
        'requests',
        'boto3',
        'gitpython',
        'service'
    ],
    python_requires='>=3.6',
)
