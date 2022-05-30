import os
from unittest import mock
from source.git import GitRepo, _find_repo_pathname


def test_git_repo_determine_pathname():
    repo_path = "git@github.com:michaelhelvey/dotfiles.git"
    path = _find_repo_pathname(repo_path)

    assert path == "dotfiles"


def test_given_no_dst_clone_returns_repo_in_current_cwd():
    with mock.patch("subprocess.check_call") as sb_mock:
        cwd = os.getcwd()
        repo = GitRepo.clone("something.git")

        expected_repo_dir = f"{cwd}/something"

        assert repo.cwd == expected_repo_dir
        sb_mock.assert_called_once_with(
            ["git", "clone", "something.git", expected_repo_dir]
        )


def test_given_dst_clone_creates_repo_in_requested_dst():
    with mock.patch("subprocess.check_call") as sb_mock:
        cwd = os.getcwd()
        repo = GitRepo.clone("something.git", "./foo/bar/blah")

        expected_repo_dir = f"{cwd}/foo/bar/blah"

        assert repo.cwd == expected_repo_dir
        sb_mock.assert_called_once_with(
            ["git", "clone", "something.git", expected_repo_dir]
        )
