# Contributing to this repository

## Licensing
If you make any contributions to this repository, you are agreeing that any
code you have contributed will be licensed under the GNU AGPL version 3 (or
any later version).

## Coding style
This repository is following the Python's PEP8 guideline:
 - https://www.python.org/dev/peps/pep-0008/
 - `pep8`/`pycodestyle` can be used to check the code compliance

You should also comment non-obvious parts of the code when possible.

## Dependencies
I want to **avoid dependencies** in this project. It does work with both
vanilla Python 2.7 and 3.9 versions. It's often trivial to make portable
code for both versions and avoid trouble such as:
 - Users can't run the project due to the Python2/3 differences
 - Issues while trying to install external dependencies on windows/linux
 - Etc.
