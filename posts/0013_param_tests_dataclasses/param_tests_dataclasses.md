# Better parameterized pytests with dataclasses

tags: Python, pytest, dataclasses

## Introduction

01_PYTEST_DATACLASSES

Parameterization is a powerful tool in pytest (the most popular Python testing framework) that allows us to write a single test with minimal code that can dynamically expand to become a bunch of similar with minor input differences. In this blog post, I will describe how to write parameterized pytests. And then, we'll expand on the topic and re-write the tests more effectively using dataclasses.

## Setup

I wrote the examples in this blog post with Python version 3.10. The only place you would notice the Python version is in how I write type hints once I introduce dataclasses:

```python
# python 3.10 type syntax
item: int | float
# python <= 3.9 type syntax
from typing import Int, Float
item: [Int, Float]
```

You'll also need to install pytest:

```bash
pip install pytest
```

[You can find the example code for this blog post all in one place here](https://github.com/VerdantFox/blog_posts/blob/main/posts/0013_param_tests_dataclasses/test_with_dataclasses.py).

## Writing tests with many variations

Let's say we want to test the following example function:

```python
def add(num1, num2):
    """Add two numbers together."""
    return num1 + num2
```

To test this extremely derivative example function, we'd want to test that various input values produce expected output values. How could we do this?

### Option 1: A series of one-off tests

One good testing practice is to make your tests small and test preferably one interaction (i.e., one function call). One way to test many inputs would be to write a series of simple, one-off tests like so:

```python
def test_add_1_2_makes_3():
    assert add(1, 2) == 3

def test_add_5_0_makes_5():
    assert add(5, 0) == 5
...
```

However, this would get very tedious, very fast, especially if we had a dozen or so different inputs we needed to test. On top of that, there would be a lot of repeated code and visual bloat. Duplicated code isn't always bad *in tests* but it would become a bit extreme if we had to write a dozen one-off tests like this.

### Option 2: Loop over inputs in a single test

To avoid repeating ourselves, we *could* write **one** function where we loop over a series of input values like so:

```python
def test_add():
    # (num1, num2, expected)
    inputs = [(1, 2, 3), (5, 0, 5), (0, 5, 5), (-5, 10, 5), (5, -10, -5)]
    for (num1, num2, expected) in inputs:
        assert add(num1, num2) == expected
```

The above solution is not ideal for two reasons.

First, if an assertion fails for one of the test cases in the `inputs` list, it would be hard to tell which test case caused the failure. In this simple example, distinguishing which case caused the assertion error would be relatively easy. Still, with more complicated inputs or tests, we might have to work hard to determine which test case caused the assertion error.

The second reason this setup is bad is that the test will fail **immediately** once we get one assertion error. We won't know if any of the input test cases *after* the first would have succeeded or failed until we find and fix the problem and re-run the test (potentially many times).

### Option 3: Use a parameterized test

The best solution is parameterized tests. Parameterized tests in pytest are powerful. They allow you to write **one** simple test with many input values. Then, at run time, your one test dynamically generates many one-off tests, each using the provided input values. An example looks like this:

```python
import pytest

# (num1, num2, expected)
ADD_CASES = [(1, 2, 3), (5, 0, 5), (0, 5, 5), (-5, 10, 5), (5, -10, -5)]


@pytest.mark.parametrize(("num1", "num2", "expected"), ADD_CASES)
def test_add_parameterized(num1, num2, expected):
    assert add(num1, num2) == expected
```

To mark a pytest as a parameterized test, we use the `@pytest.mark.parameterize` decorator. That decorator takes two input arguments. The first argument is either a string or a tuple of strings. Using the string syntax, you can pass in a comma-separated list of strings that might look like `"num1,num2,expected"`. Passing in a single item like `"num"` is also possible. The comma-separated string or tuple of strings (what we did in the above example) correspond to variable names. Then, we provide those same variable names as parameters to the test function, which we can then use as variables in the test itself.

The second input argument to `@pytest.mark.parameterize` is an iterable (for example, a list). Each item in the list will dynamically generate a new test, passing in the list item to the variable names described in the first argument of `@pytest.mark.parameterize`. If the first argument is a string variable name, each list item can be any object. However, if the first argument corresponds to *multiple* variable names, each list item must be an iterable of the same size to expand to fill out those variable names. In the above example, the list item`(1, 2, 3)` expands to fill out the variable names `("num1", "num2", "expected")`. The simplest way to do this is to pass in a list of uniform tuples like in the above example:

```python
# (num1, num2, expected)
ADD_CASES = [(1, 2, 3), (5, 0, 5), (0, 5, 5), (-5, 10, 5), (5, -10, -5)]
```

Note: I like to add a comment above the tuples to remind myself what each item in the tuple corresponds to.

In the above example, each tuple in `ADD_CASES` will generate a new test. And in each dynamically generated test, the tuple values correspond to the variables `num1, num2, expected`. For the first test case, `num1` will become `1`, `num2` will become `2`, and `expected` will become `3`. In the second test case, `num1` will become `5`, `num2` will become `0`, and `expected` will become `5`. Here's the whole example again as a reminder:

```python
# (num1, num2, expected)
ADD_CASES = [(1, 2, 3), (5, 0, 5), (0, 5, 5), (-5, 10, 5), (5, -10, -5)]


@pytest.mark.parametrize(("num1", "num2", "expected"), ADD_CASES)
def test_add_parameterized(num1, num2, expected):
    assert add(num1, num2) == expected
```

The result of running the above parameterized pytest in verbose mode looks like this:

```bash
$ pytest -k test_add_parameterized -v
========================== test session starts =========================
platform linux -- Python 3.10.12, pytest-7.4.2, /bin/python3.10
cachedir: .pytest_cache
rootdir: /my_tests
collected 5 items / 0 deselected / 5 selected                                                            

test_with_dataclasses.py::test_add_parameterized[1-2-3] PASSED    [ 20%]
test_with_dataclasses.py::test_add_parameterized[5-0-5] PASSED    [ 40%]
test_with_dataclasses.py::test_add_parameterized[0-5-5] PASSED    [ 60%]
test_with_dataclasses.py::test_add_parameterized[-5-10-5] PASSED  [ 80%]
test_with_dataclasses.py::test_add_parameterized[5--10--5] PASSED [100%]

==================== 5 passed, 0 deselected in 0.04s ====================
```

Note `-k test_add_parameterized` ran only tests containing that string in the name, and `-v` made the tests output in "verbose" mode (one line per test). Analyzing these test results, we can see that five tests ran, one for each tuple of inputs we provided. We can also see how pytest named the tests (`test_add_parameterized[1-2-3]`): the test name, with the input values of `[num1-num2-expected]` appended to the end.

Excellent! 🎉 This parameterized test is precisely what we need. We dynamically generated a series of tests for different inputs by writing one simple test (it only tests a single call of the `add` function). This approach is much cleaner and less work than writing a series of one-off tests. It is also much better than looping over these values with a single test because if one test fails, we can see which test failed, and the tests after that will continue to run. I'll change the middle test tuple to `(0, 5, 4)` to prove this.

```bash
$ pytest -k test_add_parameterized -v
=========================== test session starts ===========================
platform linux -- Python 3.10.12, pytest-7.4.2, /bin/python3.10
cachedir: .pytest_cache
rootdir: /my_tests
collected 5 items / 0 deselected / 5 selected                                                            

test_with_dataclasses.py::test_add_parameterized[1-2-3] PASSED    [ 20%]
test_with_dataclasses.py::test_add_parameterized[5-0-5] PASSED    [ 40%]
test_with_dataclasses.py::test_add_parameterized[0-5-4] FAILED    [ 60%]
test_with_dataclasses.py::test_add_parameterized[-5-10-5] PASSED  [ 80%]
test_with_dataclasses.py::test_add_parameterized[5--10--5] PASSED [100%]

================================= FAILURES =================================
____________________ test_add_parameterized[0-5-4] _________________________

num1 = 0, num2 = 5, expected = 4

    @pytest.mark.parametrize(("num1", "num2", "expected"), ADD_CASES)
    def test_add_parameterized(num1, num2, expected):
        """Test the add function using a parameterized list of tuples."""
>       assert add(num1, num2) == expected
E       assert 5 == 4
E        +  where 5 = add(0, 5)

test_with_dataclasses.py:57: AssertionError
======================== short test summary info =============================
FAILED test_with_dataclasses.py::test_add_parameterized[0-5-4] - assert 5 == 4
================= 1 failed, 4 passed, 0 deselected in 0.06 ===================
```

Notice that the middle test "FAILED", while the tests before and after that test all ran and "PASSED". Nice! 🙌

## Using pytest.param to provide test IDs

One thing I don't like about passing in a series of tuples as the second argument to `@pytest.mark.parametrize` is that the test names generated by pytest are not very expressive. Recall that the test names append all the items in the tuple, separated by dashes (e.g., `test_add_parameterized[0-5-4]`). That's not great. Luckily, we can customize our parameterized test names using `pytest.param()` objects with IDs instead of tuples. The resulting code change looks like this.

```python
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
    """Test the add function using pytest.param objects with ids set."""
    assert add(num1, num2) == expe
```

Here is the result of running the above parameterized test in verbose mode:

```bash
$ pytest -k test_add_with_ids -v
============================= test session starts =============================
platform linux -- Python 3.10.12, pytest-7.4.2 -- /bin/python3.10
cachedir: .pytest_cache
rootdir: /blog_posts
collected 5 items / 0 deselected / 5 selected                                                                    

test_with_dataclasses.py::test_add_with_ids[basic_case] PASSED            [ 20%]
test_with_dataclasses.py::test_add_with_ids[num2_has_0] PASSED            [ 40%]
test_with_dataclasses.py::test_add_with_ids[num1_has_0] PASSED            [ 60%]
test_with_dataclasses.py::test_add_with_ids[num1_negative] PASSED         [ 80%]
test_with_dataclasses.py::test_add_with_ids[num2_negative_gt_num1] PASSED [100%]

======================= 5 passed, 0 deselected in 0.04s =======================
```

Much better! Now, the dynamically generated tests have expressive names that come closer to expressing *why* each test case matters.

## The problem with passing many variables to tests

The situation laid out in the above parameterized test works well. The test is simple, and importantly, the matrix of input arguments (the `pytest.param()` iterables) is also pretty simple. But let's look at another example function that divides two numbers.

```python
def divide(num1, num2):
    """Divide two numbers."""
    return num1 / num2
```

We'll test this function like before.

```python
import pytest

DIVIDE_CASES = [
    # (num1, num2, expected)
    pytest.param(4, 2, 2, id="basic_case"),
    pytest.param(2, 4, 0.5, id="num2_gt_num1"),
    pytest.param(0, 2, 0, id="num1_0"),
]


@pytest.mark.parametrize(("num1", "num2", "expected"), DIVIDE_CASES)
def test_divide(num1, num2, expected):
    """Test the divide function using pytest.param objects with ids set."""
    assert divide(num1, num2) == expected
```

Let's say we want to test the case where `num2`, the divisor, equals `0`. That's a problem. We know that dividing a number by zero is impossible -- doing so will raise a `ZeroDivisionError`. We can expand our test for this by adding a fourth variable to our list of variables called `error`, like so.

```python
import pytest

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
```

In the above code, we use `with pytest.raises(error)`, passing in our error to let pytest know we expect an error. That code runs when `error`, passed in from `pytest.param()`, is **not** `None`. When `error` **is** `None`, we'll check that the `divide` function produces the expected outcome, like before.

> Aside: Some might say having an `if` statement in a test is bad practice. Maybe we should test the special case separately. I don't really abide by that philosophy. Furthermore, it's beside the point of this blog post.

I noticed that with four items to keep track of, the `pytest.param()` iterable has become more unwieldy. Furthermore, the last two items in the iterable (corresponding to `expected` and `error`) are a little awkward. `error` doesn't matter for cases that don't error, so we need a series of `None` filler values for `error` in those test cases. And `expected` doesn't matter for the error case since there is no expected value.

Let's expand the example one step further to drive these points home. Let's say we notice that sometimes non-numbers get passed into the `divide` function, causing more problems we need to test for. To compensate, we add a **debug** log statement to check the types of the incoming numbers.

```python
import logging
logger = logging.getLogger(__name__)


def divide_with_logging(num1, num2):
    """Divide two numbers, first logging their types in DEBUG mode."""
    logger.debug(
        "type(num1=%s, type(num2)=%s)",
        type(num1),
        type(num2),
    )
    return num1 / num2
```

We can expand our test to check for the logs under various conditions. When the log level is set to `DEBUG`, we would expect to see this **debug** log statement. When it is set to `INFO`, we would **not** expect to see the log statement.

We'll check for these conditions by adding two more arguments to our `pytest.param()` iterable: `log_level` and `log_msg`.

```python
DIVIDE_CASES_EXPANDED_WITH_LOGGING = [
    # (num1, num2, expected, error, log_level, log_msg)
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
    ("num1", "num2", "expected", "error", "log_level", "log_msg"),
    DIVIDE_CASES_EXPANDED_WITH_LOGGING,
)
def test_divide_with_logging(num1, num2, expected, error, log_level, log_msg, caplog):
    """Test the divide_with_logging method with error checking and log checking."""
    caplog.set_level(log_level)
    if error:
        with pytest.raises(error):
            divide_with_logging(num1, num2)
    else:
        assert divide_with_logging(num1, num2) == expected

    if log_msg:
        assert log_msg in caplog.text
    else:
        assert len(caplog.text) == 0
```

Before running `divide_with_logging`, we set the log level according to the passed-in `log_level` argument. After running `divide_with_logging`, we check that the log shows an expected message in cases where we expect it (when the log level is `DEBUG`) and no messages in cases where the log level is `INFO`.

Notice what has happened to our `pytest.param` iterables. Three problems developed as the test grew more complicated.

1. The `pytest.param` iterables have become **extremely** unwieldy with six items. While writing the test, I frequently lost track of which item order corresponded to which variables in the test -- meaning writing the test was more error-prone.
2. There are a lot of items in the `pytest.param` iterables that are **the same for most test iterations**. That repetitiveness is annoying to write, and having to write it every time leads to more chances for errors.
3. Updating the test 3 times meant I had to extend every `pytest.param` iterable each time so that all iterables accounted for every test variable.

For complicated parameterized tests like these, there is a better way. We can alleviate all three problems by replacing our `pytest.param` iterables with dataclass objects! 🙌

## Dataclasses

What is a dataclass? Dataclasses are just regular Python classes with extra syntactic sugar to make them easier to write and work with than traditional classes. They look like this:

```python
from dataclasses import dataclass


@dataclass
class MyDataclass:
    item_1: str
    item_2: int | None = None
    item_3: int | float = 0
```

You decorate a class with the `@dataclass` decorator to indicate it is a dataclass. Then, you can directly define instance attributes (attributes set at instantiation) on the class. These instance attributes **must** have type hints, or you'll get an error that the variable is not defined. You can set default values for the attributes by setting the attribute `=` to something. Note that even though you **must** add type hints to the dataclass attributes, they are not enforced at runtime when set.

This is what it looks like when we instantiate the above dataclass:

```python
>>> my_dataclass_instance = MyDataclass(item_1="blah", item_2=7)
>>> print(my_dataclass_instance)
MyDataclass(item_1='blah', item_2=7, item_3=0)
```

Notice that dataclasses also provide pretty `print` strings out of the box. You could accomplish (roughly) the same goal with a traditional Python class like so.

```python
class MyNormalClass:

    def __init__(
        self,
        item_1: str,
        item_2: int | None = None,
        item_3: int | float = 0
    ):
        self.item_1: str = item_1
        self.item_2: int | None = item_2
        self.item_3: int | float = item_3

    def __str__(self):
        return f"MyNormalClass(item_1={self.item_1}, item_2={self.item_2}, item_3={self.item_3})"
```

```python
>>> my_normal_class_instance = MyNormalClass(item_1="blah", item_2=7)
>>> print(my_normal_class_instance)
MyNormalClass(item_1=blah, item_2=7, item_3=0)
```

I think we can all agree that writing classes the `dataclass` way is much easier (both to write and to read).

## Writing parameterized tests with dataclasses

Let's re-write our complicated test for `divide_with_logging` using a dataclass for each test case in the parameterized test instead of a `pytest.param` iterable.

First, we'll define the dataclass we'll use for each test case in the parameterized test.

```python
from dataclasses import dataclass

@dataclass
class DivideTestCase:
    """Test case for testing the divide_with_logging function."""

    id: str
    num1: Any
    num2: Any
    expected: int | float | None = None
    error: Exception | None = None
    log_level: str = logging.INFO
    log_msg: str | None = None
```

Notice a couple of things about the test case.

1. We're using a dataclass to write it, so it looks very clean.
2. We include a required `id` attribute. Later, we'll use this for the test `id` values.
3. `num1` and `num2` are **required** attributes (like `id`). They are **required** because they don't have a default value set. These are attributes that make sense to set individually for every test.
4. `expected`, `error`, `log_level`, and `log_msg` are **optional** attributes. They have default values set that make sense for most tests (or at least for many tests). These are attributes that we no longer need to worry about for tests that don't use them or for tests that typically use them the same way almost every time.
5. The type hints will help with auto-complete when we write the actual test cases.

Next, we add the test cases for the parameterized test:

```python
DIVIDE_TEST_CASES = [
    DivideTestCase(num1=4, num2=2, expected=2, id="basic_case"),
    DivideTestCase(num1=2, num2=4, expected=0.5, id="num2_gt_num1"),
    DivideTestCase(num1=0, num2=2, expected=0, id="num1_0"),
    DivideTestCase(num1=2, num2=0, error=ZeroDivisionError, id="num2_0"),
    DivideTestCase(
        num1=6,
        num2=2,
        expected=3,
        log_level=logging.DEBUG,
        log_msg="num1=<class 'int'>, type(num2)=<class 'int'>",
        id="debug_basic_case",
    ),
    DivideTestCase(
        num1=5,
        num2=2.5,
        expected=2,
        log_level=logging.DEBUG,
        log_msg="num1=<class 'int'>, type(num2)=<class 'float'>",
        id="debug_int_float",
    ),
    DivideTestCase(
        num1=4,
        num2="2",
        error=TypeError,
        log_level=logging.DEBUG,
        log_msg="num1=<class 'int'>, type(num2)=<class 'str'>",
        id="num1_0",
    ),
]
```

These test cases are much easier to read and write than the `pytest.param` style test cases. Here is an example comparison of the last test case for each:

```python
# pytest.param style
pytest.param(
    4,
    "2",
    None,
    TypeError,
    logging.DEBUG,
    "num1=<class 'int'>, type(num2)=<class 'str'>",
    id="debug_int_str",
)
# dataclass style
DivideTestCase(
    num1=4,
    num2="2",
    error=TypeError,
    log_level=logging.DEBUG,
    log_msg="num1=<class 'int'>, type(num2)=<class 'str'>",
    id="num1_0",
)
```

Why is the latter example better?

1. It is structured as key-value pairs instead of arguments. It is much easier to determine which key a value belongs to than the order of arguments in an iterable.
2. The sane default values in the dataclass mean we don't have to specify every key-value pair for every test.
3. We get editor support while writing the key-value pairs.
4. It's easy to expand the test cases. If we add a new attribute with a default value set, we don't have to change any of our old test cases to use it.

Finally, we add the test itself.

```python
import pytest

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

    if test_case.log_msg:
        assert test_case.log_msg in caplog.text
    else:
        assert len(caplog.text) == 0
```

First, let's discuss the top bit:

```python
@pytest.mark.parametrize(
    "test_case",
    [
        pytest.param(test_case, id=test_case.id)
        for test_case in DIVIDE_CASES_WITH_DATACLASSES
    ],
)
```

We define a single variable name, "test_case". Then we use a list comprehension to wrap our dataclass objects in a `pytest.param` iterable containing one item, the dataclass object. Along the way, we supply our dataclass' `id` attribute to the `pytest.param` id argument so our tests continue to have meaningful names.

```python
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

    if test_case.log_msg:
        assert test_case.log_msg in caplog.text
    else:
        assert len(caplog.text) == 0
```

We provide the `test_case` parameter defined in `pytest.mark.parameterize` in the test definition. Then, all the variables we defined in `DivideTestCase` become accessible as object attributes like `test_case.error`, `test_case.num1`, `test_case.num2`. Clean right? For completeness, here's the whole test, not broken up into pieces:

```python
@dataclass
class DivideTestCase:
    """Test case for testing the divide_with_logging function."""

    id: str
    num1: Any
    num2: Any
    expected: int | float | None = None
    error: Exception | None = None
    log_level: str = logging.INFO
    log_msg: str | None = None


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
        log_msg="num1=<class 'int'>, type(num2)=<class 'int'>",
        id="debug_basic_case",
    ),
    DivideTestCase(
        num1=5,
        num2=2.5,
        expected=2,
        log_level=logging.DEBUG,
        log_msg="num1=<class 'int'>, type(num2)=<class 'float'>",
        id="debug_int_float",
    ),
    DivideTestCase(
        num1=4,
        num2="2",
        error=TypeError,
        log_level=logging.DEBUG,
        log_msg="num1=<class 'int'>, type(num2)=<class 'str'>",
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

    if test_case.log_msg:
        assert test_case.log_msg in caplog.text
    else:
        assert len(caplog.text) == 0
```

The result of running those tests looks like this.

```bash
$ pytest -k test_divide_with_logging_and_dataclass -v
======================================= test session starts =======================================
platform linux -- Python 3.10.12, pytest-7.4.2 -- /blog_posts/venv/bin/python3.10
cachedir: .pytest_cache
rootdir: /blog_posts
collected 7 items / 0 deselected / 7 selected                                                                                      

test_with_dataclasses.py::test_divide_with_logging_and_dataclass[basic_case] PASSED         [ 14%]
test_with_dataclasses.py::test_divide_with_logging_and_dataclass[num2_gt_num1] PASSED       [ 28%]
test_with_dataclasses.py::test_divide_with_logging_and_dataclass[num1_00] PASSED            [ 42%]
test_with_dataclasses.py::test_divide_with_logging_and_dataclass[num2_0] PASSED             [ 57%]
test_with_dataclasses.py::test_divide_with_logging_and_dataclass[debug_basic_case] PASSED   [ 71%]
test_with_dataclasses.py::test_divide_with_logging_and_dataclass[debug_int_float] PASSED    [ 85%]
test_with_dataclasses.py::test_divide_with_logging_and_dataclass[num1_01] PASSED            [100%]

================================= 7 passed, 0 deselected in 0.04s =================================
```

## Conclusions

Parameterized tests are a powerful way of writing one test to dynamically generate a range of similar tests, subbing out some of the data for each test. They offer a way to reduce code duplication in your tests without looping over all your data in an individual test.

In a parameterized test, you can supply as many variables as you want in a tuple or `pytest.param` object to make them available in your test. However, having too many variables is unwieldy. If you find yourself writing a parameterized test with many variables, try using a dataclass to contain all those variables, especially if it makes sense for some variables to set default values.

I hope you found this guide to parameterized testing with pytest helpful. If you are interested in more pytest tips and tricks, check out my other blog post, [9 pytest tips and tricks to take your tests to the next level](/blog/view/9-pytest-tips-and-tricks-to-take-your-tests-to-the-next-level).
