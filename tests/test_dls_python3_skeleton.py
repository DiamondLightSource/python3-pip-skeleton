import subprocess
import sys
from configparser import ConfigParser
from os import makedirs
from pathlib import Path

import pytest

from python3_pip_skeleton import __main__, __version__


def check_output(*args, cwd=None) -> str:
    try:
        return subprocess.check_output(
            args, stderr=subprocess.STDOUT, text=True, cwd=cwd
        )
    except subprocess.CalledProcessError as e:
        raise ValueError(e.output)


def test_cli_version():
    output = check_output(sys.executable, "-m", "python3_pip_skeleton", "--version")
    assert output.strip() == __version__


def test_new_module(tmp_path: Path):
    module = tmp_path / "my-module"
    output = check_output(
        sys.executable,
        "-m",
        "python3_pip_skeleton",
        "new",
        "--org=myorg",
        "--package=my_module",
        "--full-name=Firstname Lastname",
        "--email=me@myaddress.com",
        str(module),
    )
    assert output.strip().endswith(
        "Instructions on how to develop this module are in CONTRIBUTING.rst"
    )

    conf = ConfigParser()
    conf.read(module / "setup.cfg")
    assert conf["metadata"]["author"] == "Firstname Lastname"
    assert conf["metadata"]["author_email"] == "me@myaddress.com"
    versiongit_lines = [
        line
        for line in (module / "docs" / "reference" / "api.rst").read_text().splitlines()
        if "setuptools" in line
    ]
    assert (
        "    Version number as calculated by https://github.com/pypa/setuptools_scm"
        in versiongit_lines
    )
    assert (module / "src" / "my_module").is_dir()
    assert check_output("git", "branch", cwd=module).strip() == "* main"
    check_output("virtualenv", ".venv", cwd=module)
    check_output(".venv/bin/pip", "install", ".[dev]", cwd=module)
    check_output(
        ".venv/bin/sphinx-build",
        "-EWT",
        "--keep-going",
        "docs",
        "build/html",
        cwd=module,
    )
    with pytest.raises(ValueError) as ctx:
        check_output(module / ".venv/bin/pytest", "tests", cwd=module)
    out = ctx.value.args[0]
    print(out)
    assert "6 failed, 4 passed" in out
    assert "Please change description in ./setup.cfg" in out
    assert "Please change ./README.rst" in out
    assert "Please change ./docs/reference/api.rst" in out
    assert "Please delete ./docs/how-to/accomplish-a-task.rst" in out
    assert "Please delete ./docs/explanations/why-is-something-so.rst" in out


def test_new_module_existing_dir(tmp_path: Path):
    module = tmp_path / "my-module"
    makedirs(module / "existing_dir")

    with pytest.raises(Exception) as excinfo:
        check_output(
            sys.executable,
            "-m",
            "python3_pip_skeleton",
            "new",
            "--org=myorg",
            "--package=my_module",
            "--full-name=Firstname Lastname",
            "--email=me@myaddress.com",
            str(module),
        )
    assert "to not exist, or be an empty dir" in str(excinfo.value)


def test_existing_module(tmp_path: Path):
    module = tmp_path / "scanspec"
    __main__.git(
        "clone",
        "--depth",
        "1",
        "--branch",
        "0.5.3",
        "https://github.com/dls-controls/scanspec",
        str(module),
    )
    output = check_output(
        sys.executable,
        "-m",
        "python3_pip_skeleton",
        "existing",
        str(module),
    )
    assert output.endswith(
        """
Automatic merge failed; fix conflicts and then commit the result.

Please fix the conflicts above, then you can run:
    git branch -d skeleton-merge-branch
Instructions on how to develop this module are in CONTRIBUTING.rst
"""
    )
    __main__.git("merge", "--abort", cwd=str(module))
    MERGE_BRANCH = "skeleton-merge-branch"

    with pytest.raises(Exception) as excinfo:
        output = check_output(
            sys.executable,
            "-m",
            "python3_pip_skeleton",
            "existing",
            str(module),
        )
    assert (
        f"{MERGE_BRANCH} already exists. \
                Please run 'python3-pip-skeleton clean' to remove it."
        in str(excinfo.value)
    )

    branches = __main__.list_branches(module)
    assert MERGE_BRANCH in branches
    output = check_output(
        sys.executable,
        "-m",
        "python3_pip_skeleton",
        "clean",
        ".",
        cwd=str(module),
    )
    assert output.strip("\n") == f"{MERGE_BRANCH} deleted from existing repo"
    branches = __main__.list_branches(module)
    assert MERGE_BRANCH not in branches


def test_existing_module_already_adopted(tmp_path: Path):
    module = tmp_path / "scanspec"
    __main__.git(
        "clone",
        "--branch",
        "0.5.4",  # dls-python3-skeleton was adopted in this release
        "https://github.com/dls-controls/scanspec",
        str(module),
    )
    with pytest.raises(Exception) as excinfo:
        check_output(
            sys.executable,
            "-m",
            "python3_pip_skeleton",
            "existing",
            str(module),
        )
    assert "already adopted skeleton" in str(excinfo.value)
