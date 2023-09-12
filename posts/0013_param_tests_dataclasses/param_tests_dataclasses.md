# Better parameterized pytests with dataclasses

tags: Python, pytest, dataclasses

## Introduction

01_PYTEST_DATACLASSES

Parameterization is a powerful tool in pytest (the most popular python testing framework) that allow us to quickly write a bunch of very similar tests with a minimal amount of code. In this blog post I will lay out how to write parameterized pytests the standard way (with tuples) and then how to write those same tests with dataclasses, and I'll explain why the latter approach might be better in many cases, especially for more complicated tests.

## Setup

The examples in this blog post were written with python version 3.10. This only matters for convenience around type hint syntax in the dataclass which looks like this:

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

[The example code can for this post can be found all in one place here](https://github.com/VerdantFox/blog_posts/blob/main/posts/0013_param_tests_dataclasses/test_with_dataclasses.py).

## Writing tests with many variations

Let's say we want to test the following example function:

```python
def add(num1, num2):
    """Add two numbers together."""
    return num1 + num2
```

To test this extremely derivative example function, we'd want to test that a variety of input values produce expected output values. How would we do this?

### Option 1: a series of one-off tests

One good testing practice is to make your tests small and try to test preferably one interaction (i.e. one function call). One way to test many inputs would be to write a series of simple, one-off tests like so:

```python
def test_add_1_2_makes_3():
    assert add(1, 2) == 3

def test_add_5_0_makes_5():
    assert add(5, 0) == 5
...
```

However, this would get very tedious, very fast, especially if we had a dozen or so different inputs we needed to test. On top of that there would be a lot of repeated code and visual bloat. Repeated code isn't always bad *in tests* but, it would become a bit extreme if we had to write a dozen one off tests like this.

### Option 2: loop over inputs in a single test

To avoid repeating ourselves, we *could* write **one** function where we loop over a series of input values like so:

```python
def test_add():
    # (num1, num2, expected)
    inputs = [(1, 2, 3), (5, 0, 5), (0, 5, 5), (-5, 10, 5), (5, -10, -5)]
    for (num1, num2, expected) in inputs:
        assert add(num1, num2) == expected
```

This is not an ideal solution for 2 reasons.

One, if an assertion fails for one of the test cases in the `inputs` list, it would be hard to tell which test case caused the failure. Admittedly, in this simple example, it would't be too difficult to distinguish which case caused the assertion error, but with more complicated inputs or more complicated tests, we might have to work hard to figure out which test case caused the assertion error.

The second reason this setup is bad is because as soon as we get one assertion error, the test will fail. We won't know if any of the input test cases *after* the first would have succeeded or failed until we find and fix the problem and re-run the test (potentially many times).

### Option 3: use a parameterized test

The solution is parameterized tests. Parameterized tests in pytest are powerful. They allow you to write one, simple test with many input values. The result is that at run time, your one test gets split into many one-off tests, each using the provided input values. An example looks like this:

```python
import pytest

# (num1, num2, expected)
ADD_CASES = [(1, 2, 3), (5, 0, 5), (0, 5, 5), (-5, 10, 5), (5, -10, -5)]


@pytest.mark.parametrize(("num1", "num2", "expected"), ADD_CASES)
def test_add_parameterized(num1, num2, expected):
    assert add(num1, num2) == expected
```

To mark a pytest as a parameterized test we use the `@pytest.mark.parameterize` decorator. That decorator takes 2 input arguments. The first argument is either a string or a tuple of strings. If using the string syntax, you can pass in a comma-separated list of strings that might look like this: `"num1,num2,expected"`. It's also possible to just pass in a single item like: `"num"`. That comma-separated string or tuple of strings (what we did in the example) correspond to variable names. In the test function, we pass in the exact same variable names as function parameters that we can use in the test.

The second input argument to `@pytest.mark.parameterize` is an iterable (for example, a list). That iterable should contain a series of items. This is what gets passed into the variable or variables provided by the first argument. If the first argument was a string for a single variable name, the iterable items could be anything. They don't even need to be of the same type. For example:

```python
import pytest

THINGS = ["cheesburger", 25, float, {"foo": "bar"}]


@pytest.mark.parametrize("random_object", THINGS)
def test_add_parameterized(random_object):
    assert random_object is not None
```

If the first argument to `@pytest.mark.parameterize` was a tuple or a comma-separated string, each item in the iterable needs to be an iterable of exactly the length of the number of variables provided by the first argument. The simplest way to do this is to pass in a list of uniform tuples like in the above example:

```python
# (num1, num2, expected)
ADD_CASES = [(1, 2, 3), (5, 0, 5), (0, 5, 5), (-5, 10, 5), (5, -10, -5)]
```

I like to put a comment above the tuples to remind myself what each item in the tuple corresponds to. In the above example, for the first test case, `num1` would become `1`, `num2` would become `2` and `expected` would become `3`. In the second test case, `num1` would become `5`, `num2` would become `0`, and `expected` would become `5`. And so... each tuple in the list generating a separate test case. Then we can use the generated variables for dynamically generated tests

```python
# (num1, num2, expected)
ADD_CASES = [(1, 2, 3), (5, 0, 5), (0, 5, 5), (-5, 10, 5), (5, -10, -5)]


@pytest.mark.parametrize(("num1", "num2", "expected"), ADD_CASES)
def test_add_parameterized(num1, num2, expected):
    assert add(num1, num2) == expected
```

The result of running the above parameterized test in verbose mode looks like this:

```bash
$ pytest -k test_add_parameterized -v
=========================================== test session starts ============================================
platform linux -- Python 3.10.12, pytest-7.4.2, /bin/python3.10
cachedir: .pytest_cache
rootdir: /my_tests
collected 5 items / 0 deselected / 5 selected                                                            

test_with_dataclasses.py::test_add_parameterized[1-2-3] PASSED    [ 20%]
test_with_dataclasses.py::test_add_parameterized[5-0-5] PASSED    [ 40%]
test_with_dataclasses.py::test_add_parameterized[0-5-5] PASSED    [ 60%]
test_with_dataclasses.py::test_add_parameterized[-5-10-5] PASSED  [ 80%]
test_with_dataclasses.py::test_add_parameterized[5--10--5] PASSED [100%]

===================================== 5 passed, 29 deselected in 0.04s =====================================
```

Note `-k test_add_parameterized` ran only tests containing that string in the name and `-v` made the tests output in "verbose" mode (one line per test). Analyzing these test results, we can see that, indeed, 5 tests ran, one for each tuple of inputs we provided. We can also see how pytest named the tests (`test_add_parameterized[1-2-3]`): the test name, with the input values of `[num1-num2-expected]` appended to the end.

Awesome! 🎉 Our parameterized test is exactly what we need. By writing a simple test (it only tests a single call of the `add` function), we were able to dynamically generate a series of different test that all test different input functions to our test. This is much cleaner and much less work than writing a series of one off functions. And it is much better than looping over these values with a single test because if one test fails, we can clearly see which test failed and the tests thereafter will continue to run. To prove this I'll change the middle test tuple to `(0, 5, 4)`.

```bash
$ pytest -k test_add_parameterized -v
=========================================== test session starts ============================================
platform linux -- Python 3.10.12, pytest-7.4.2, /bin/python3.10
cachedir: .pytest_cache
rootdir: /my_tests
collected 5 items / 0 deselected / 5 selected                                                            

test_with_dataclasses.py::test_add_parameterized[1-2-3] PASSED    [ 20%]
test_with_dataclasses.py::test_add_parameterized[5-0-5] PASSED    [ 40%]
test_with_dataclasses.py::test_add_parameterized[0-5-4] FAILED    [ 60%]
test_with_dataclasses.py::test_add_parameterized[-5-10-5] PASSED  [ 80%]
test_with_dataclasses.py::test_add_parameterized[5--10--5] PASSED [100%]

================================================= FAILURES =================================================
______________________________________ test_add_parameterized[0-5-4] _______________________________________

num1 = 0, num2 = 5, expected = 4

    @pytest.mark.parametrize(("num1", "num2", "expected"), ADD_CASES)
    def test_add_parameterized(num1, num2, expected):
        """Test the add function using parameterized list of tuples."""
>       assert add(num1, num2) == expected
E       assert 5 == 4
E        +  where 5 = add(0, 5)

test_with_dataclasses.py:57: AssertionError
========================================= short test summary info ==========================================
FAILED test_with_dataclasses.py::test_add_parameterized[0-5-4] - assert 5 == 4
================================ 1 failed, 4 passed, 0 deselected in 0.06s ================================
```

Noticed the middle test "FAILED", while the tests before and after that test all ran and "PASSED". Nice! 🙌

## Using pytest.param to provide test ids

One thing I don't like about passing in a series of tuples as the second argument to `@pytest.mark.parametrize` is the test names generated by pytest are not very expressive. Recall that the names just append all the objects in the tuple, separated by dashes (e.g. `test_add_parameterized[0-5-4]`). Or if the passed in objects are too complicated to output as strings, it'll write something like `test_add_parameterized[my_value1]`. That's not great. Luckily you can customize the test name of a set of inputs for parameterized test to whatever you like by passing special `pytest.param()` objects with ids instead of tuples. The result looks like this.

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
    """Test the add function, using pytest.param objects with ids set."""
    assert add(num1, num2) == expe
```

When I run the above parameterized test in verbose mode, the result looks like this.

```bash
$ pytest -k test_add_with_ids -v
=============================================== test session starts ================================================
platform linux -- Python 3.10.12, pytest-7.4.2 -- /bin/python3.10
cachedir: .pytest_cache
rootdir: /home/teddy/projects/blog_posts
collected 5 items / 0 deselected / 5 selected                                                                    

test_with_dataclasses.py::test_add_with_ids[basic_case] PASSED            [ 20%]
test_with_dataclasses.py::test_add_with_ids[num2_has_0] PASSED            [ 40%]
test_with_dataclasses.py::test_add_with_ids[num1_has_0] PASSED            [ 60%]
test_with_dataclasses.py::test_add_with_ids[num1_negative] PASSED         [ 80%]
test_with_dataclasses.py::test_add_with_ids[num2_negative_gt_num1] PASSED [100%]

========================================= 5 passed, 29 deselected in 0.04s =========================================
```

Much better! Now the dynamically generated tests have expressive names that come closer to expressing *why* each test case is important.

## The problem with passing many variables to tests

## Dataclasses

## Writing parameterized tests with dataclasses

## Conclusions