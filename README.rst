dls-python3-skeleton
===========================

|code_ci| |docs_ci| |coverage| |pypi_version| |license|

This skeleton module (inspired by `jaraco/skeleton
<https://blog.jaraco.com/skeleton/>`_) is a generic Python project structure
which provides a means to keep tools and techniques in sync between multiple
Python projects.

============== ==============================================================
PyPI           ``pip install dls-python3-skeleton``
Source code    https://github.com/dls-controls/dls-python3-skeleton
Documentation  https://dls-controls.github.io/dls-python3-skeleton
Releases       https://github.com/dls-controls/dls-python3-skeleton/releases
============== ==============================================================

It integrates the following tools:

- Pipenv for version management
- Pre-commit with black, flake8, isort and mypy for static analysis
- Pytest for code and coverage
- Sphinx for tutorials, how-to guides, explanations and reference documentation
- GitHub Actions for code and docs CI and deployment to PyPI and GitHub Pages
- If you use VSCode, it will run black, flake8, isort and mypy on save

The ``skeleton`` branch of this module contains the source code that can be
merged into new or existing projects, and pulled from to keep them up to date.
It can also serve as a working example for those who would prefer to
cherry-pick.

The ``master`` branch contains the
docs and a command line tool to ease the adoption of this skeleton into new::

    dls-python3-skeleton new /path/to/be/created

and existing projects::

    dls-python3-skeleton existing /path/to/existing/repo

.. |code_ci| image:: https://github.com/dls-controls/dls-python3-skeleton/workflows/Code%20CI/badge.svg?branch=master
    :target: https://github.com/dls-controls/dls-python3-skeleton/actions?query=workflow%3A%22Code+CI%22
    :alt: Code CI

.. |docs_ci| image:: https://github.com/dls-controls/dls-python3-skeleton/workflows/Docs%20CI/badge.svg?branch=master
    :target: https://github.com/dls-controls/dls-python3-skeleton/actions?query=workflow%3A%22Docs+CI%22
    :alt: Docs CI

.. |coverage| image:: https://codecov.io/gh/dls-controls/dls-python3-skeleton/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/dls-controls/dls-python3-skeleton
    :alt: Test Coverage

.. |pypi_version| image:: https://img.shields.io/pypi/v/dls-python3-skeleton.svg
    :target: https://pypi.org/project/dls-python3-skeleton
    :alt: Latest PyPI version

.. |license| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
    :target: https://opensource.org/licenses/Apache-2.0
    :alt: Apache License

..
    Anything below this line is used when viewing README.rst and will be replaced
    when included in index.rst

See https://dls-controls.github.io/dls-python3-skeleton for more detailed documentation.
