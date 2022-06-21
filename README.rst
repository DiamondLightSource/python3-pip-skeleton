python3-pip-skeleton
===========================

|code_ci| |docs_ci| |coverage| |pypi_version| |license|

This skeleton module (inspired by `jaraco/skeleton
<https://blog.jaraco.com/skeleton/>`_) is a generic Python project structure
which provides a means to keep tools and techniques in sync between multiple
Python projects.

============== ==============================================================
PyPI           ``pip install python3-pip-skeleton``
Source code    https://github.com/epics-containers/python3-pip-skeleton
Documentation  https://epics-containers.github.io/python3-pip-skeleton
Releases       https://github.com/epics-containers/python3-pip-skeleton/releases
============== ==============================================================

It integrates the following tools:

- pip and setuptools_scm for version management
- Pre-commit with black, flake8 and isort for static analysis
- Pytest for tests and code git@github.com:dls-controls/python3-pip-skeleton.gitcoverage
- Sphinx for tutorials, how-to guides, explanations and reference documentation
- GitHub Actions for code and docs CI and deployment to PyPI and GitHub Pages
- tox -p: runs pre-commit, pytest, mypy and make docs
  - which verifies all the things that CI does
- If you use VSCode, it will run black, flake8, isort and mypy on save

The ``skeleton`` branch of this module contains the source code that can be
merged into new or existing projects, and pulled from to keep them up to date.
It can also serve as a working example for those who would prefer to
cherry-pick.

The ``main`` branch contains the
docs and a command line tool to ease the adoption of this skeleton into new::

    python3-pip-skeleton new /path/to/be/created

and existing projects::

    python3-pip-skeleton existing /path/to/existing/repo

.. |code_ci| image:: https://github.com/epics-containers/python3-pip-skeleton/workflows/Code%20CI/badge.svg?branch=main
    :target: https://github.com/epics-containers/python3-pip-skeleton/actions?query=workflow%3A%22Code+CI%22
    :alt: Code CI

.. |docs_ci| image:: https://github.com/epics-containers/python3-pip-skeleton/workflows/Docs%20CI/badge.svg?branch=main
    :target: https://github.com/epics-containers/python3-pip-skeleton/actions?query=workflow%3A%22Docs+CI%22
    :alt: Docs CI

.. |coverage| image:: https://codecov.io/gh/epics-containers/python3-pip-skeleton/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/epics-containers/python3-pip-skeleton
    :alt: Test Coverage

.. |pypi_version| image:: https://img.shields.io/pypi/v/python3-pip-skeleton.svg
    :target: https://pypi.org/project/python3-pip-skeleton
    :alt: Latest PyPI version

.. |license| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
    :target: https://opensource.org/licenses/Apache-2.0
    :alt: Apache License

..
    Anything below this line is used when viewing README.rst and will be replaced
    when included in index.rst

See https://epics-containers.github.io/python3-pip-skeleton for more detailed documentation.
