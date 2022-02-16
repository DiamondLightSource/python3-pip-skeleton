import re
import shutil
from argparse import ArgumentParser
from configparser import ConfigParser
from pathlib import Path
from subprocess import STDOUT, CalledProcessError, check_output
from tempfile import TemporaryDirectory

from . import __version__

__all__ = ["main"]

# The source of the skeleton module to pull from
SKELETON = "https://github.com/dls-controls/dls-python3-skeleton"
# The name of the merge branch that will be created
MERGE_BRANCH = "skeleton-merge-branch"
# Extensions to change
CHANGE_SUFFIXES = [".py", ".rst", ".cfg", ""]
# Files not to change
IGNORE_FILES = ["CHANGELOG.rst", "test_boilerplate_removed.py", "_version_git.py"]
# Ranges to ignore between
IGNORE_RANGES = {
    "CONTRIBUTING.rst": ("\nUpdating the tools\n", None),
    "api.rst": (
        "Version number as calculated by",
        "https://github.com/dls-controls/versiongit",
    ),
}


def git(*args, cwd=None) -> str:
    command = ["git"] + [str(x) for x in args]
    try:
        return check_output(command, stderr=STDOUT, cwd=cwd, text=True)
    except CalledProcessError as e:
        print(e.output)
        raise


class GitTemporaryDirectory(TemporaryDirectory):
    def __enter__(self):
        return self

    def __call__(self, *args) -> str:
        return git(*args, cwd=self.name)

    def __truediv__(self, other) -> Path:
        return Path(self.name) / other


def merge_skeleton(
    path: Path,
    org: str,
    full_name: str,
    email: str,
    package,
):
    path = path.resolve()
    repo = path.name

    def replace_text(text: str) -> str:
        text = text.replace("dls-controls", org)
        text = text.replace("dls-python3-skeleton", repo)
        text = text.replace("dls_python3_skeleton", package)
        text = text.replace("Firstname Lastname", full_name)
        text = text.replace("email@address.com", email)
        return text

    with GitTemporaryDirectory() as git_tmp:
        # Clone existing repo into tmp so we don't mess up if we fail
        # half way through
        git_tmp("clone", path, git_tmp.name)
        # We will use this branch to put the skeleton changes on
        git_tmp("checkout", "--orphan", MERGE_BRANCH)
        # Delete all the current files if there are any
        git_tmp("rm", "-rf", ".", "--ignore-unmatch")
        # And make sure src isn't there otherwise the git mv below
        # will do the wrong thing
        shutil.rmtree(git_tmp / "src", ignore_errors=True)
        # Merge in the skeleton commits
        git_tmp("pull", SKELETON, "skeleton")
        # Move things around
        git_tmp("mv", "src/dls_python3_skeleton", f"src/{package}")
        git_tmp("mv", "tests/test_dls_python3_skeleton.py", f"tests/test_{package}.py")
        # Change contents of all children known to git
        for relative_child in git_tmp("ls-files").splitlines():
            child = Path(git_tmp.name) / relative_child
            if child.suffix in CHANGE_SUFFIXES and child.name not in IGNORE_FILES:
                text = child.read_text()
                start_search, end_search = IGNORE_RANGES.get(child.name, (None, None))
                if start_search:
                    start_ignore = text.find(start_search)
                    assert start_ignore > 0, f"{start_search} not in {child.name}"
                    if end_search:
                        end_ignore = text.find(end_search, start_ignore) + len(
                            end_search
                        )
                        assert end_ignore > 0, f"{end_search} not in {child.name}"
                    else:
                        end_ignore = len(text)
                else:
                    start_ignore = 0
                    end_ignore = 0
                child.write_text(
                    replace_text(text[:start_ignore])
                    + text[start_ignore:end_ignore]
                    + replace_text(text[end_ignore:])
                )
        # Commit what we have and push to the original repo
        git_tmp("commit", "-a", "-m", f"Rename dls-python3-skeleton -> {repo}")
        git_tmp("push", "origin", MERGE_BRANCH)
    try:
        git("merge", MERGE_BRANCH, "--allow-unrelated-histories", cwd=path)
    except CalledProcessError:
        # The merge failed, so ask the user to fix it
        print("Please fix the conflicts above, then you can run:")
        print(f"    git branch -d {MERGE_BRANCH}")
    else:
        git("branch", "-d", MERGE_BRANCH, cwd=path)
    print("Instructions on how to develop this module are in CONTRIBUTING.rst")


def validate_package(args) -> str:
    package = args.package or args.path.name
    valid = re.match("[a-zA-Z][a-zA-Z_0-9]*$", package)
    assert valid, f"'{package}' is not a valid python package name"
    return package


def new(args):
    path: Path = args.path

    if path.exists():
        assert path.is_dir() and not list(
            path.iterdir()
        ), f"Expected {path} to not exist, or be an empty dir"
    else:
        path.mkdir(parents=True)

    package = validate_package(args)
    git("init", cwd=path)
    print(f"Created git repo in {path}")
    merge_skeleton(
        path=path,
        org=args.org,
        full_name=args.full_name or git("config", "--get", "user.name").strip(),
        email=args.email or git("config", "--get", "user.email").strip(),
        package=package,
    )


def existing(args):
    path: Path = args.path

    assert path.is_dir(), f"Expected {path} to be an existing directory"
    package = validate_package(args)
    conf = ConfigParser()
    conf.read(path / "setup.cfg")
    merge_skeleton(
        path=args.path,
        org=args.org,
        full_name=conf["metadata"]["author"],
        email=conf["metadata"]["author_email"],
        package=package,
    )


def main(args=None):
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()
    parser.add_argument("--version", action="version", version=__version__)
    # Add a command for making a new repo
    sub = subparsers.add_parser("new", help="Make a new repo forked from this skeleton")
    sub.set_defaults(func=new)
    sub.add_argument("path", type=Path, help="Path to new repo to create")
    sub.add_argument(
        "--org", default="dls-controls", help="GitHub org, default dls-controls"
    )
    sub.add_argument(
        "--package", default=None, help="Package name, defaults to directory name"
    )
    sub.add_argument(
        "--full-name", default=None, help="Full name, defaults to git config user.name"
    )
    sub.add_argument(
        "--email", default=None, help="Email address, defaults to git config user.email"
    )
    # Add a command for adopting in existing repo
    sub = subparsers.add_parser("existing", help="Adopt skeleton in existing repo")
    sub.set_defaults(func=existing)
    sub.add_argument("path", type=Path, help="Path to new repo to existing repo")
    sub.add_argument(
        "--org", default="dls-controls", help="GitHub org, default dls-controls"
    )
    sub.add_argument(
        "--package", default=None, help="Package name, defaults to directory name"
    )
    # Parse args and run
    args = parser.parse_args(args)
    args.func(args)


if __name__ == "__main__":
    main()
