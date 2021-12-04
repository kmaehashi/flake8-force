# flake8-force

Flake8 extension to provide `force-check` option.

When this option is enabled, flake8 performs all checks even if the target file cannot be interpreted as a Python source code (e.g., when there is a syntax error in the file).

This extension was written to bring back the behavior of flake8 3.x in flake 4.0+ to lint against Cython code.

Usage:
* Specify the option via command line: ``flake8 --force-check ...``
* Add `force-check = True` to flake8 configuration file
