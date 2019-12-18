import sys
from os import path

from setuptools import setup  # type: ignore

BUILD = 0
VERSION = "0.9.2"
RELEASE = VERSION

if __name__ == "__main__":
    readme = path.join(path.dirname(path.abspath(__file__)), "README.md")
    with open(readme, "r") as f:
        long_desc = f.read()

    setup(
        name="pytiled_parser",
        version=RELEASE,
        description="Python Library for parsing Tiled Map Editor maps.",
        long_description=long_desc,
        author="Benjamin Kirkbride",
        author_email="BenjaminKirkbride@gmail.com",
        license="MIT",
        url="https://github.com/Beefy-Swain/pytiled_parser",
        download_url="https://github.com/Beefy-Swain/pytiled_parser",
        install_requires=["attrs"],
        packages=["pytiled_parser"],
        classifiers=[
            "Development Status :: 1 - Planning",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: Implementation :: CPython",
            "Topic :: Software Development :: Libraries :: Python Modules",
        ],
        test_suite="tests",
    )
