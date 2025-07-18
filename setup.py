from setuptools import setup, find_packages

setup(
    name="bitnet-api",
    version="0.1.0",
    author="Axel Sheire",
    description="Client for Microsoft BitNet Demo API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/umm-dev/bitnet-api",
    packages=find_packages(),
    install_requires=["requests>=2.25"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    ],
    python_requires=">=3.7",
)
