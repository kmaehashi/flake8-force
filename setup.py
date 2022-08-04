import os

import setuptools


def _read(path):
    with open(os.path.join(os.path.dirname(__file__), path)) as f:
        return f.read()


# Get `__version__`
exec(_read("src/flake8_force/_version.py"))


setuptools.setup(
    name="flake8-force",
    license="MIT",
    version=__version__,  # NOQA
    description="flake8 extension to force running check",
    long_description=_read("README.md"),
    long_description_content_type="text/markdown",
    author="Kenichi Maehashi",
    url="https://github.com/kmaehashi/flake8-force",
    package_dir={"": "src/"},
    packages=["flake8_force"],
    entry_points={
        "flake8.extension": [
            "FRC000 = flake8_force:Flake8Force",
        ],
    },
    install_requires=['flake8'],
    classifiers=[
        "Framework :: Flake8",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
)
