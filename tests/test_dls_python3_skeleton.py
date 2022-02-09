import subprocess
import sys
from configparser import ConfigParser
from pathlib import Path

import pytest

from dls_python3_skeleton import __main__, __version__


def check_output(*args, cwd=None) -> str:
    try:
        return subprocess.check_output(
            args, stderr=subprocess.STDOUT, text=True, cwd=cwd
        )
    except subprocess.CalledProcessError as e:
        raise ValueError(e.output)


def test_cli_version():
    output = check_output(sys.executable, "-m", "dls_python3_skeleton", "--version")
    assert output.strip() == __version__


def test_new_module(tmp_path: Path):
    module = tmp_path / "my-module"
    output = check_output(
        sys.executable,
        "-m",
        "dls_python3_skeleton",
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
        if "versiongit" in line
    ]
    assert (
        "    Version number as calculated by https://github.com/dls-controls/versiongit"
        in versiongit_lines
    )
    assert (module / "src" / "my_module").is_dir()
    assert check_output("git", "branch", cwd=module).strip() == "* master"
    check_output("pipenv", "install", "--dev", cwd=module)
    check_output("pipenv", "run", "docs", cwd=module)
    with pytest.raises(ValueError) as ctx:
        check_output("pipenv", "run", "tests", cwd=module)
    out = ctx.value.args[0]
    print(out)
    assert "6 failed, 5 passed" in out
    assert "Please change description in ./setup.cfg" in out
    assert "Please change ./README.rst" in out
    assert "Please change ./docs/reference/api.rst" in out
    assert "Please delete ./docs/how-to/accomplish-a-task.rst" in out
    assert "Please delete ./docs/explanations/why-is-something-so.rst" in out


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
        "dls_python3_skeleton",
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
