import re

import pytest

from conftest import assert_bash_exec


@pytest.mark.bashcomp(ignore_env=r"^-declare -f _tar$")
class TestTar:

    @pytest.fixture(scope="class")
    def gnu_tar(self, bash):
        got = assert_bash_exec(bash, "tar --version || :", want_output=True)
        if not re.search(r"\bGNU ", got):
            pytest.skip("Not GNU tar")

    @pytest.mark.complete("tar ")
    def test_1(self, completion):
        assert completion

    # Test "f" when mode is not as first option
    @pytest.mark.complete("tar zfc ", cwd="tar")
    def test_2(self, completion):
        assert completion == "dir/ dir2/".split()

    @pytest.mark.complete("tar cf ", cwd="tar")
    def test_3(self, completion):
        assert completion == "dir/ dir2/".split()

    @pytest.mark.complete("tar tf archive.tar.xz dir/file", cwd="tar")
    def test_4(self, completion):
        assert completion == "dir/fileA dir/fileB dir/fileC".split()

    @pytest.mark.complete("tar cTfvv NOT_EXISTS DONT_CREATE.tar ", cwd="tar")
    def test_5(self, completion):
        assert completion == \
            "archive.tar.xz dir/ dir2/ escape.tar".split()

    @pytest.mark.complete("tar xvf ", cwd="tar")
    def test_6(self, completion):
        assert completion == \
            "archive.tar.xz dir/ dir2/ escape.tar".split()

    @pytest.mark.complete("tar -c")
    def test_7(self, completion, gnu_tar):
        """Test short options."""
        assert completion

    @pytest.mark.complete("tar -zcf ", cwd="tar")
    def test_8(self, completion, gnu_tar):
        """Test mode not as first option."""
        assert completion == "dir/ dir2/".split()

    @pytest.mark.complete("tar -cf ", cwd="tar")
    def test_9(self, completion, gnu_tar):
        """Test that we don't suggest rewriting existing archive."""
        assert completion == "dir/ dir2/".split()

    @pytest.mark.complete("tar -c --file ", cwd="tar")
    def test_10(self, completion, gnu_tar):
        assert completion == "dir/ dir2/".split()

    @pytest.mark.complete("tar -cvv --file ", cwd="tar")
    def test_11(self, completion, gnu_tar):
        assert completion == "dir/ dir2/".split()

    @pytest.mark.complete("tar -tf archive.tar.xz dir/file", cwd="tar")
    def test_12(self, completion, gnu_tar):
        """Test archive listing."""
        assert completion == "dir/fileA dir/fileB dir/fileC".split()

    @pytest.mark.complete("tar -t --file archive.tar.xz dir/file", cwd="tar")
    def test_13(self, completion, gnu_tar):
        """Test archive listing with --file."""
        assert completion == "dir/fileA dir/fileB dir/fileC".split()

    @pytest.mark.complete("tar --block")
    def test_14(self, completion, gnu_tar):
        assert completion == "--block-number --blocking-factor=".split()

    @pytest.mark.complete("tar --add-fil")
    def test_15(self, completion, gnu_tar):
        assert completion == "--add-file="
        assert not completion.endswith(" ")

    @pytest.mark.complete("tar -cf /dev/null --posi")
    def test_16(self, completion, gnu_tar):
        assert completion == "--posix"
        assert completion.endswith(" ")

    @pytest.mark.complete("tar --owner=")
    def test_17(self, bash, completion, gnu_tar):
        users = sorted(assert_bash_exec(
            bash, "compgen -A user", want_output=True).split())
        assert completion == users

    @pytest.mark.complete("tar --group=")
    def test_18(self, bash, completion, gnu_tar):
        groups = sorted(assert_bash_exec(
            bash, "compgen -A group", want_output=True).split())
        assert completion == groups

    # Use -b for this as -b is still not handled by tar's completion
    @pytest.mark.complete("tar -cvvfb ")
    def test_19(self, bash, completion, gnu_tar):
        """Test short option -XXXb <TAB> (arg required)."""
        assert not completion
