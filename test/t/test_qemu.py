import pytest


class TestQemu:

    @pytest.mark.complete("qemu ")
    def test_1(self, completion):
        assert completion
