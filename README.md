# flake8-force

Flake8 extension that provides `force-check` option.

When this option is enabled, flake8 performs all checks even if the target file cannot be interpreted as a Python source code (e.g., when there is a syntax error in the file).

This extension was written to bring back the behavior of flake8 v3.x in flake8 v4.0+ to lint against Cython code.
Note that the option is ineffective in flake8 v3.x or earlier.

## Installation

```sh
pip install flake8-force
```

## Usage

* Specify the option via the command line: `flake8 --force-check ...`.
* Add `force-check = True` to the flake8 configuration file.
