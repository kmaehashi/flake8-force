# flake8-force

[![PyPI](https://img.shields.io/pypi/v/flake8-force.svg)](https://pypi.python.org/pypi/flake8-force)
[![Test](https://github.com/kmaehashi/flake8-force/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/kmaehashi/flake8-force/actions/workflows/test.yml)

Flake8 extension that provides `force-check` option.

When this option is enabled, flake8 performs all checks even if the target file cannot be interpreted as a Python source code (e.g., when there is a syntax error in the file).

This extension was written to bring back the behavior of flake8 v3.x in flake8 v4.0+ to lint against Cython code.
Note that the option is ineffective in flake8 v3.x or earlier.

## Installation

```sh
pip install flake8-force
```

## Usage

You can enable the `flake8-force` plugin by either:

* Specifying the option via the command line: `flake8 --force-check ...`.
* Adding `force-check = True` to the flake8 configuration file.

## Tips for checking Cython code

While this extension "forces" flake8 to ignore problems with parsing Cython syntax as Python code, flake8 must be separately configured to permit Cython syntax through ignoring certain rules.
The configuration below is suggested for that purpose.
Some projects may not need to ignore every rule, depending on the use of Cython.
The [pycodestyle docs](https://pycodestyle.pycqa.org/en/latest/intro.html#error-codes) define what each rule means.

```ini
[flake8]
filename = *.py,*.pyx,*.pxd,*.pxi
ignore = E203,E225,E226,E227,E402,E741,E901,E999,W503,W504
force-check = True
```

## Pre-commit hook

The configuration below can be used with [pre-commit](https://pre-commit.com/) to install this extension alongside flake8 and enable checking Cython files.
Also see the [flake8 docs on version control hooks](https://flake8.pycqa.org/en/latest/user/using-hooks.html).

```yaml
-   repo: https://github.com/PyCQA/flake8
    rev: ''  # Pick a git hash / tag to point to
    hooks:
    -   id: flake8
        types: ["file"]  # Override the default types (only python)
        types_or: ["python", "cython"]  # Support both python and cython types
        additional_dependencies: ["flake8-force"]  # Add this extension
```
