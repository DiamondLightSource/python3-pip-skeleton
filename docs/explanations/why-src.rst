Why use a source directory
==========================

This skeleton repo has made the decision to use a source directory. The reasons
for this are set out in `Hynek's article`_ and summarized below.

.. _Hynek's article: https://hynek.me/articles/testing-packaging/

The main advantage is that the source directory cannot shadow installed packages
as it would if it was in the root of the repository. This means that if you
install the package, then run the tests, they will run against the installed
package and not the source directory, testing for packaging bugs.

A secondary advantage is symmetry, sources go in ``src/``, tests go in
``tests\``, docs go in ``docs``.

This is tested in CI in the following way:

- ``wheel`` job creates a wheel, then installs it in an isolated environment and
  runs the cli. This checks ``install_requirements`` are sufficient to run the
  cli.
- ``test`` job with ``pipenv: deploy`` does an `editable install`_ of the
  package. This is the mode that is used at development time, as modifications
  to sources can be tested without reinstalling.
- ``test`` job with ``pipenv: skip-lock`` does a regular install, which
  checks that all files needed for the tests are packaged with the distribution.

.. _editable install: https://pip.pypa.io/en/stable/cli/pip_install/#editable-installs
