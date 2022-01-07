Creating a new repo from the skeleton
=====================================

Once you have followed the `installation` tutorial, you can use the
commandline tool to make a new repo that inherits the skeleton::

    dls-python3-skeleton new /path/to/be/created

This will:

- Take the repo name from the last element of the path
- Take the package name from the repo name unless overridden by ``--package``
- Create a new repo at the requested path, forked from the skeleton repo
- Create a single commit that modifies the skeleton with the repo and package name

.. note::

    If you installed the commandline tool in a virtualenv, be sure to run
    ``deactivate`` when you have finished running it, otherwise ``pipenv
    install`` will use your virtualenv rather than making its own

Getting started with your new repo
----------------------------------

Your new repo has a workflow based on pipenv. The first thing to do is to use
pipenv to install packages in a virtual environment::

    pipenv install --dev

You can then use the ``pipenv run`` command to run shell commands within this
virtual environment. For instance::

    pipenv run python

will run the python interpreter with access to all the packages you need to
develop your repo.

Running the tests
-----------------

There are also some extra convenience scripts that ``pipenv run`` knows about::

    pipenv run tests

will run ``pytest`` to find all the unit tests and run them. The first time you
run this, there will be some failing tests::

    ============================================================================ short test summary info ============================================================================
    FAILED tests/test_boilerplate_removed.py::test_module_description - AssertionError: Please change description in ./setup.cfg to be a one line description of your module
    FAILED tests/test_boilerplate_removed.py::test_changed_README_intro - AssertionError: Please change ./README.rst to include an intro on what your module does
    FAILED tests/test_boilerplate_removed.py::test_changed_README_body - AssertionError: Please change ./README.rst to include some features and why people should use it
    FAILED tests/test_boilerplate_removed.py::test_removed_CHANGELOG_note - AssertionError: Please change ./CHANGELOG.rst To remove the note at the top
    FAILED tests/test_boilerplate_removed.py::test_changed_CHANGELOG - AssertionError: Please change ./CHANGELOG.rst To summarize changes to your module as you make them
    FAILED tests/test_boilerplate_removed.py::test_docs_ref_api_changed - AssertionError: Please change ./docs/reference/api.rst to introduce the API for your module
    FAILED tests/test_boilerplate_removed.py::test_how_tos_written - AssertionError: Please delete ./docs/how-to/accomplish-a-task.rst and write some docs/how-tos
    FAILED tests/test_boilerplate_removed.py::test_explanations_written - AssertionError: Please delete ./docs/explanations/why-is-something-so.rst and write some docs/explanations
    ========================================================================== 8 failed, 5 passed in 0.28s ==========================================================================

When you change the template text mentioned in the error, these tests will pass.
If you intend to fix the test later, you can mark the tests as "expected to
fail" by adding a decorator to the relevant function. For example:

.. code-block:: python

    @pytest.mark.xfail(reason="docs not written yet")
    def test_explanations_written():
        ...

Building the docs
-----------------

There is also a convenience script for building the docs::

    pipenv run docs

You can then view the docs output with a web browse::

    firefox build/html/index.html

Pushing to GitHub
-----------------

To push the resulting repo to GitHub, first create an empty repo from the GitHub
website, then run the following::

    git remote add $(cat .gitremotes)
    git push -u github master

This will then run the continuous integration (CI) jobs, which run the tests and
build the docs using the commands above.

Once the docs build has passed, you can use the Settings on the repo page on the
GitHub website to enable github pages publishing of the ``gh-pages`` branch.

What next?
----------

Now you can make the repo your own, add code, write docs, delete what you don't
like, then push a tag and CI will make a release and push it to PyPI. Look at
the `../how-to` for articles on these and other topics.
