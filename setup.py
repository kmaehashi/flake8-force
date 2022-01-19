import setuptools

setuptools.setup(
    name="flake8-force",
    license="MIT",
    version="0.0.1",
    description="flake8 extension to force running check",
    author="Kenichi Maehashi",
    url="https://github.com/kmaehashi/flake8-force",
    package_dir={"": "src/"},
    packages=["flake8_force"],
    entry_points={
        "flake8.extension": [
            "flake8_force = flake8_force:Flake8Force",
        ],
    },
    classifiers=[
        "Framework :: Flake8",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
)
