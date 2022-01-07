Why use pre-commit
==================

There are a number of things that CI needs to run:

- pytest
- black
- mypy
- flake8
- isort

The initial approach this module took was to integrate everything
under pytest that had a plugin, and isort under flake8:

- pytest

  - pytest-black
  - pytest-mypy
  - pytest-flake8

    - flake8-isort

This had the advantage that a ``pipenv run tests`` run in CI would catch and
report all test failures, but made each run take longer than it needed to. Also,
flake8 states that it `does not have a public, stable, Python API
<https://flake8.pycqa.org/en/latest/user/python-api.html>`_ so did not
recommend the approach taken by pytest-flake8.

To address this, the tree was rearranged:

- pytest
- black
- mypy
- flake8

  - flake8-isort

If using VSCode, this will still run black, flake8 and mypy on file save, but
for those using other editors and for CI another solution was needed. Enter
`pre-commit <https://pre-commit.com/>`_. This allows hooks to be run at ``git
commit`` time on just the files that have changed, as well as on all tracked
files by CI. All that is needed is a one time install of the git commit hook::

  $ pipenv run pre-commit install

The graph now looks like:

- pytest
- pre-commit

  - black
  - mypy
  - flake8
  - flake8-isort

Now the workflow looks like this:

- Save file, VSCode runs black, flake8 and mypy on it
- Run pytest until tests pass
- Commit files and pre-commit runs black, flake8 and mypy on them
- Push to remote and CI runs black, flake8, mypy once on all files, then pytest
  multiple times in a test matrix
