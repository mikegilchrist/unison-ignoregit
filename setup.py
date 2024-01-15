import os
from os.path import join, exists
from setuptools import find_packages, setup

base_dir = os.path.dirname(__file__)
readme_path = join(base_dir, "README.md")
if exists(readme_path):
    with open(readme_path) as stream:
        long_description = stream.read()
else:
    long_description = ""

setup(
    name="unison-ignoregit",
    install_requires=["pathspec==0.10.3"],
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description="A unison wrapper to integrate with git ls-files output.",
    long_description="A wrapper for the file synchronization program `unison` which excludes anyfile that is git software related (e.g. .git/) or controlled by git.  Wrapper based on [unison-ignoregit](https://github.com/lime-green/unison-gitignore)" 
    long_description_content_type="text/markdown",
    author="Mike Gilchrist",
    url="https://github.com/mikegilchrist/unison-ignoregit",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    entry_points={
        "console_scripts": [
            "unison-ignoregit = unison_ignoregit.__main__:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    license="MIT",
    keywords=["unison", "ignoregit"],
)
