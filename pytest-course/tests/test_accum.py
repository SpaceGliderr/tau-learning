import pytest


@pytest.mark.accumulator
def test_accumulator_init(accum):
    """Verifies new instance starts with count of 0."""
    assert accum.count == 0


@pytest.mark.accumulator
def test_accumulator_add_one(accum):
    """Verifies `add` method adds one to the internal count when it is called without other arguments."""
    accum.add()
    assert accum.count == 1


@pytest.mark.accumulator
def test_accumulator_add_three(accum):
    """Verifies `add` method adds 3 to the count when it is called with an argument method of 3."""
    accum.add(3)
    assert accum.count == 3


@pytest.mark.accumulator
def test_accumulator_add_twice(accum):
    """Verifies count increases appropriately with multiple add called."""
    accum.add()
    accum.add()
    assert accum.count == 2


@pytest.mark.accumulator
def test_accumulator_cannot_set_count_directly(accum):
    """Verifies count attribute cannot be assigned directly because it is read-only."""
    with pytest.raises(AttributeError, match=r"has no setter") as e:
        accum.count = 10