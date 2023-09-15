"""Example parameterized pytests with dataclasses."""
import logging
from dataclasses import dataclass
from typing import Any

import pytest

logger = logging.getLogger(__name__)


def add(num1, num2):
    """Add two numbers."""
    return num1 + num2


def divide(num1, num2):
    """Divide two numbers."""
    return num1 / num2


def divide_with_logging(num1, num2):
    """Divide two numbers, first logging their types in DEBUG mode."""
    logger.debug(
        "type(num1=%s, type(num2)=%s)",
        type(num1),
        type(num2),
    )
    return num1 / num2

# OPTION 1: 1 off tests (BAD)
def test_add_1_2_returns_3():
    """Test that adding 1 and 2 returns 3 (1 off tests, BAD)."""
    assert add(1, 2) == 3


def test_add_5_0_returns_5():
    """Test that adding 5 and 0 returns 5 (1 off tests, BAD)."""


# OPTION 2: loop in test (BAD)
def test_add():
    """Test add function by looping over inputs (BAD)."""
    # (num1, num2, expected)
    inputs = [(1, 2, 3), (5, 0, 5), (0, 5, 5), (-5, 10, 5), (5, -10, -5)]
    for (num1, num2, expected) in inputs:
        assert add(num1, num2) == expected


# OPTION 3: Parameterized tests (GOOD)
# (num1, num2, expected)
ADD_CASES = [(1, 2, 3), (5, 0, 5), (0, 5, 4), (-5, 10, 5), (5, -10, -5)]


@pytest.mark.parametrize(("num1", "num2", "expected"), ADD_CASES)
def test_add_parameterized(num1, num2, expected):
    """Test the add function using parameterized list of tuples."""
    assert add(num1, num2) == expected


ADD_CASES_WITH_IDS = [
    # (num1, num2, expected)
    pytest.param(1, 2, 3, id="basic_case"),
    pytest.param(5, 0, 5, id="num2_has_0"),
    pytest.param(0, 5, 5, id="num1_has_0"),
    pytest.param(-5, 10, 5, id="num1_negative"),
    pytest.param(5, -10, -5, id="num2_negative_gt_num1"),
]


@pytest.mark.parametrize(("num1", "num2", "expected"), ADD_CASES_WITH_IDS)
def test_add_with_ids(num1, num2, expected):
    """Test the add function, using pytest.param objects with ids set."""
    assert add(num1, num2) == expected


DIVIDE_CASES = [
    # (num1, num2, expected)
    pytest.param(4, 2, 2, id="basic_case"),
    pytest.param(2, 4, 0.5, id="num2_gt_num1"),
    pytest.param(0, 2, 0, id="num1_0"),
]


@pytest.mark.parametrize(("num1", "num2", "expected"), DIVIDE_CASES)
def test_divide(num1, num2, expected):
    """Test the divide function, using pytest.param objects with ids set."""
    assert divide(num1, num2) == expected


DIVIDE_CASES_EXPANDED = [
    # (num1, num2, expected, error)
    pytest.param(4, 2, 2, None, id="basic_case"),
    pytest.param(2, 4, 0.5, None, id="num2_gt_num1"),
    pytest.param(0, 2, 0, None, id="num1_0"),
    pytest.param(2, 0, None, ZeroDivisionError, id="num1_0"),
]


@pytest.mark.parametrize(("num1", "num2", "expected", "error"), DIVIDE_CASES_EXPANDED)
def test_divide_with_error(num1, num2, expected, error):
    """Test the divide function with added error catching and pytest.param."""
    if error:
        with pytest.raises(error):
            divide(num1, num2)
    else:
        assert divide(num1, num2) == expected


DIVIDE_CASES_EXPANDED_WITH_LOGGING = [
    # (num1, num2, expected, error, log_level, expected_log_msg)
    pytest.param(4, 2, 2, None, logging.INFO, "", id="basic_case"),
    pytest.param(2, 4, 0.5, None, logging.INFO, "", id="num2_gt_num1"),
    pytest.param(0, 2, 0, None, logging.INFO, "", id="num1_0"),
    pytest.param(2, 0, None, ZeroDivisionError, logging.INFO, "", id="num2_0"),
    pytest.param(
        6,
        2,
        3,
        None,
        logging.DEBUG,
        "num1=<class 'int'>, type(num2)=<class 'int'>",
        id="debug_basic_case",
    ),
    pytest.param(
        5,
        2.5,
        2,
        None,
        logging.DEBUG,
        "num1=<class 'int'>, type(num2)=<class 'float'>",
        id="debug_int_float",
    ),
    pytest.param(
        4,
        "2",
        None,
        TypeError,
        logging.DEBUG,
        "num1=<class 'int'>, type(num2)=<class 'str'>",
        id="debug_int_str",
    ),
]


@pytest.mark.parametrize(
    ("num1", "num2", "expected", "error", "log_level", "expected_log_msg"),
    DIVIDE_CASES_EXPANDED_WITH_LOGGING,
)
def test_divide_with_logging(num1, num2, expected, error, log_level, expected_log_msg, caplog):
    """Test the divide_with_logging method with error checking and log checking."""
    caplog.set_level(log_level)
    if error:
        with pytest.raises(error):
            divide_with_logging(num1, num2)
    else:
        assert divide_with_logging(num1, num2) == expected

    if expected_log_msg:
        assert expected_log_msg in caplog.text
    else:
        assert len(caplog.text) == 0


@dataclass
class DivideTestCase:
    """Test case for testing the divide_with_logging function."""

    id: str
    num1: Any
    num2: Any
    expected: int | float | None = None
    error: Exception | None = None
    log_level: str = logging.INFO
    expected_log_msg: str | None = None


DIVIDE_CASES_WITH_DATACLASSES = [
    DivideTestCase(num1=4, num2=2, expected=2, id="basic_case"),
    DivideTestCase(num1=2, num2=4, expected=0.5, id="num2_gt_num1"),
    DivideTestCase(num1=0, num2=2, expected=0, id="num1_0"),
    DivideTestCase(num1=2, num2=0, error=ZeroDivisionError, id="num2_0"),
    DivideTestCase(
        num1=6,
        num2=2,
        expected=3,
        log_level=logging.DEBUG,
        expected_log_msg="num1=<class 'int'>, type(num2)=<class 'int'>",
        id="debug_basic_case",
    ),
    DivideTestCase(
        num1=5,
        num2=2.5,
        expected=2,
        log_level=logging.DEBUG,
        expected_log_msg="num1=<class 'int'>, type(num2)=<class 'float'>",
        id="debug_int_float",
    ),
    DivideTestCase(
        num1=4,
        num2="2",
        error=TypeError,
        log_level=logging.DEBUG,
        expected_log_msg="num1=<class 'int'>, type(num2)=<class 'str'>",
        id="num1_0",
    ),
]


@pytest.mark.parametrize(
    "test_case",
    [
        pytest.param(test_case, id=test_case.id)
        for test_case in DIVIDE_CASES_WITH_DATACLASSES
    ],
)
def test_divide_with_logging_and_dataclass(
    test_case: DivideTestCase, caplog: pytest.LogCaptureFixture
):
    """Test the divide_with_logging function using dataclass objects."""
    caplog.set_level(test_case.log_level)
    if test_case.error:
        with pytest.raises(test_case.error):
            divide_with_logging(test_case.num1, test_case.num2)
    else:
        assert divide_with_logging(test_case.num1, test_case.num2) == test_case.expected

    if test_case.expected_log_msg:
        assert test_case.expected_log_msg in caplog.text
    else:
        assert len(caplog.text) == 0
