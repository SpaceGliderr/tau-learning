import pytest
from src.accum import Accumulator


@pytest.fixture
def accum():
    return Accumulator()
