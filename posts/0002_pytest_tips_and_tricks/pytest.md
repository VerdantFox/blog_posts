# 9 pytest tips and tricks to take your tests to the next level

tags: testing, pytest, python

## Introduction

PYTEST_IMAGE

Are you a python developer looking to improve your testing abilities with
pytest? Me too! So I've put together a list of 9 tips and tricks I've
found most useful in getting my tests looking sharp. Here are the features
we're going to be covering today:

1. Useful command-line arguments
2. `skip` and `xfail`
3. Mocking with `monkeypatch`
4. `tmp_path` and `importlib`
5. `fixture`s and the `conftest.py` file
6. Testing python exceptions
7. Checking stdout and log messages
8. Parameterizing tests
9. Using pytest-cov

All of the code discussed in this article can be found in the following
[GitHub repository](https://github.com/VerdantFox/pytest_examples){: target="_blank", rel="noopener noreferrer" }
I created. To run the code, you'll need `pytest` and `pytest-cov`, which you
can install with `pip install pytest` and `pip install pytest-cov`.
I recommend doing so in a virtual environment.

## Setup

First, we'll take a quick look at the example code that we are going to
create tests for. The code contains a fairly simple `Math` class, with a
few simple static methods: `add()`, `divide()`, `multiply()`, which simply
perform that action on two numbers, along with `slow()` which just sleeps for
an amount of time set by the global variable `GLOBAL_SLEEP_SECONDS`. Next,
there's a function called `some_math_function` which takes two numbers as
parameters and uses all the above-mentioned class methods in sequence,
and prints and logs some messages based on how long it took.

Also in the module are three other unrelated example functions that will
help with explaining various pytest tricks. These include
`update_file_via_pathlib()` which will update a file given a pathlib path,
`error_function()` which will raise an error if the parameter passed to it
is `True`, and `environment_var_function()` which will return a message
based on an environment variable.

I'll show the entirety of this module here for your reference.

`src/example.py`

```python
"""example: file with example python code to pytest"""
import logging
import os
import time

LOGGER = logging.getLogger(__name__)
GLOBAL_SLEEP_SECS = 3
DEBUG_MODE = False


class Math:
    """ Class with simple math functions to test """

    @staticmethod
    def add(first, second):
        """ Add two numbers"""
        return first + second

    @staticmethod
    def divide(first, second):
        """ Divide two numbers (excluding remainder)  """
        return first // second

    @staticmethod
    def multiply(first, second):
        """ Multiply two numbers"""
        return first * second

    @staticmethod
    def slow():
        """ just slow down our main function """
        print(f"SLEEPING {GLOBAL_SLEEP_SECS} seconds!")
        time.sleep(GLOBAL_SLEEP_SECS)


def some_math_function(first, second, half=False):
    """ Some function using Math """
    before = time.time()
    math = Math()
    addition = math.add(first, second)
    division = math.divide(first, second)
    math.slow()
    solution = math.multiply(addition, division)
    after = time.time()
    if after - before > 2:
        LOGGER.warning("warning message!")
        LOGGER.info("info message!")
        print("print message")
    if DEBUG_MODE:
        LOGGER.debug("Only in debug!")
    if half:
        solution /= 2

    return solution


def update_file_via_pathlib(path):
    """ Get the contents of an input pathlib file object """
    contents = path.read_text()
    new_contents = "Check this out: " + contents.strip() + " BAM!"
    path.write_text(new_contents)
    return new_contents


def error_function(raise_error):
    """ Function will raise an error if you'd like it to """
    if raise_error:
        raise RuntimeError("Alas, there is an error!")
    return True


def environment_var_function():
    """ Some function that deals with environment variables """
    if os.environ.get("MY_VAR") == "true":
        return "MY_VAR is set to 'true'"
    else:
        return "MY_VAR is not set to 'true'"


if __name__ == "__main__":  # pragma: no cover
    # This code won't get run by tests
    print(some_math_function(2, 1))
```

Now let's get on to testing this code with my top ten pytest tips and tricks.

## 1. Useful command-line arguments

Here's my list of most useful command-line arguments along with short
descriptions. I'll explain in more detail below:

```text
-s (show std_out even if the test passes)
-k STRING (run test with STRING in the name)
-m MARKER (run tests containing a marker)
-v (verbose output -- show each test's name)
--tb=LENGTH (adjust the length of traceback messages)
--lf (re-run only the tests that failed)
--durations=n (see execution times for n slowest tests)
```

### -s

Sometimes you want to see messages to standard out (usually `print()` messages).
These messages are normally captured and hidden from the user. They are only
shown for failed tests -- after the error stack trace is shown. If you want
to see messages to standard out for ALL tests, while the tests are running,
use the `pytest -s` switch.

### -k STRING

The most basic command to run all your tests is simply calling `pytest`. Pytest
will search through your packages, find modules labeled `test_something` or
`something_test`, and then run all the functions that start with `test_`. You
can run against a specific folder or file with `pytest folder_name` or
`pytest file_name`. But say you want to run only a specific test or a subset
of tests. You can do so with `pytest -k STRING`. This will select only
tests that contain `STRING` in their name. If I had a test called
`test_basic`, I could run this test with `pytest -k test_basic`.
Notice this would also test a test named `test_basic_code` because
`test_basic` is also in that name.

### -m MARKER

Sometimes you might want to consistently run a subset of tests together
and exclude other tests. You can `mark` these tests with a name of your
choice and run them later with `pytest -m MARK`. Let's look at an example:

My test file:

```python
import pytest

def test_basic():
    ...

@pytest.mark.slow
def test_complicated():
    ...
```

If I were to run `pytest -m slow`, only the tests containing the
`@pytest.mark.slow` decorator (`test_complicated()`) would be run.
Furthermore, I could run `pytest -m "not slow"` to run all tests that
do not contain the `@pytest.mark.slow` decorator (`test_basic()`).

When creating markers, you'll also want to list your markers in your
`pytest.ini` file at the route of your project, otherwise pytest will
warn that you might have a typo in your marker name. The `pytest.ini` file
for the above example might look something like this:

```ini
[pytest]
markers =
    slow: tests that run slowly
```

### -v

A normal pytest run will list a module name followed by a series of `.`s,
one for each passed test or `F`s, one for each failed test.
ie (`example_test.py .FF..`). You might want to see the name of each test
as they are run to quickly see which tests passed and which
tests failed. To do so use the `-v` (for verbose) flag. The same run tests might look
something like this:

```text
src/example_test.py::test_basic PASSED
src/example_test.py::test_complicated FAILED
src/example_test.py::test_other FAILED
src/example_test.py::test_easy PASSED
src/example_test.py::test_thing PASSED
```

This verbose output showing specific test names is especially useful when
debugging parametrized tests (see tip number 9 for more on parametrized
testing).

### --tb=LENGTH

When a test fails, you'll see a "traceback message". These are the messages
that show what the error was in your code, and where it's located.
The normal pytest traceback message is great. It's color-coded and super
detailed, so you can find out exactly what went wrong with your test. If
you're running a lot of tests and several "FAILURE"s occur though, those
messages can become very noisy. Introducing `--tb=LENGTH`. This argument
allows you to adjust the traceback message style to suit your needs. My
favorite "LENGTH" arguments are `short`, `line`, and `no`. I'll show how
their output looks below.

Here's an example test for our `src/example.py` file:

```python
def test_failure():
    """ A test designed to fail, will raise ZeroDivisionError """
    example.Math().divide(1, 0)
```

Here's the standard traceback message (or `--tb=auto`):

```text
    @pytest.mark.failing
    def test_failure():
        """ A test designed to fail, will raise ZeroDivisionError """
>       example.Math().divide(1, 0)

src/example_test.py:30: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

first = 1, second = 0

    @staticmethod
    def divide(first, second):
        """ Divide two numbers (excluding remainder)  """
>       return first // second
E       ZeroDivisionError: integer division or modulo by zero

src/example.py:22: ZeroDivisionError
```

Here's with `--tb=short`:

```text
src/example_test.py:30: in test_failure
    example.Math().divide(1, 0)
src/example.py:22: in divide
    return first // second
E   ZeroDivisionError: integer division or modulo by zero
```

Here's with `--tb=line`:

```text
/path/to/src/example.py:22: ZeroDivisionError: integer division or modulo by zero
```

With `--tb=no` you will not see any traceback. This can be useful if you just
want to find out *which* tests fail, then you can re-test an individual test
with a longer traceback to find out *why* it failed.

### --lf/--last-failed

This command-line switch is convenient when you have a subset of your
tests failing. You can run `pytest --lf`, make changes to try to fix the
failing tests, and then repeat the command over to only run tests that
failed on the previous run until all tests pass.

### --durations=n

The "durations" command line argument is super useful for timing your tests.
After all tests have run, it reports back the `n` slowest tests, with their
execution times. It will even distinguish between a test function's "call",
"setup" and "teardown" so you can see if it is the test itself ("call") that
is slow or the is it just the "setup" functions (fixtures) that are slow. If
`--durations=0`, all test execution times will be reported back. Here is an
example of what we see with `--durations=3` for our example test suite.

```text
================== slowest 3 durations ==================
3.00s call     src/example_test.py::test_capsys
3.00s call     src/example_test.py::test_caplog_debug
3.00s call     src/example_test.py::test_caplog_standard
```

## 2. `skip` and `xfail`

Occasionally tests just don't work the way you want them to, or maybe
they test a feature that isn't implemented yet. Even though
these tests fail right now, you'd like to keep them around and
fix them in the future. Introducing `skip` and `xfail`.

### `skip`

To mark a test to be skipped under all circumstances, decorate the
test function with a `skip` marker like so:

```python
@pytest.mark.skip(reason="No way of testing this properly")
def test_skipped():
    """ Mark a test to be always skipped with a reason (marked as s or SKIPPED) """
    assert False
```

Now when you run your tests, this test will show up as an `s` under a normal
run. Under a `verbose` (`-v`) run the output will show `SKIPPED (REASON)` (for
the above test `SKIPPED (No way of testing this properly)`). If you only want
to `skip` a test under certain conditions, mark with `skipif` like so:

```python
@pytest.mark.skipif(
    os.environ.get("SKIP") != "1", reason="It only works if SKIP is set to '1'"
)
def test_skipped_if():
    """ Mark a test to be skipped under certain conditions with a reason """
    assert True
```

Notice, the first argument to the `skipif` decorator resolves to a *boolean*
(`True` or `False`) value which will `skip` the test if the *boolean* value
resolves to `True` or run test normally if the value resolves to `False`.

### `xfail`

Another option if you know your test fails under certain conditions, is to
mark it as `xfail`. This says, "Yes, I know this test fails,
but I want to leave it as is and not see a "FAILED" message or traceback.
Marking a test for `xfail` looks like this:

```python
@pytest.mark.xfail(
    condition=os.environ.get("MY_VAR") == "true",
    reason="It should fail if MY_VAR is set to 'true'",
)
def test_xfail():
    """ Mark a test to be expected to fail under conditions  """
    assert example.environment_var_function() == "MY_VAR is not set to 'true'"
```

Notice my first parameter is `condition`. Just like with `skipif`, I make a
*boolean* condition where the test is known to fail. If that condition is *not*
met, the test is run *normally*. If that condition *is* met, the test is run
as an `xfail` (meaning you expect the test to fail). If the test *does* fail
(as expected), the result is marked with a lower case `x` (or `XFAIL (REASON)`
in verbose mode). If the test *passes* (not expected), the result is marked
with an upper case `X`, or `XPASS (REASON)` in verbose mode.

## 3. Mocking with `monkeypatch`

Sometimes things are a little too complicated, slow, or just out of your
control for you to effectively test a section of code. In this case,
you need to mock that functionality to get your test to run properly.
`monkeypatch` is the built-in way to mock objects in pytest. With `monkeypatch`,
you can mock global variables, functions and methods, class attributes,
or even environment variables. Here are some examples of how to use `monkeypatch`
for your mocking needs.

### Mock a global variable

Recall, one of the main functions we are testing in `example.py` is
`some_math_function()`. This function calls the `Math.slow()` method,
which sleeps for `GLOBAL_SLEEP_SECONDS` (where `GLOBAL_SLEEP_SECONDS`) is
an environment variable that is sed to 3 seconds at the top of the module.
In the following test we will mock `GLOBAL_SLEEP_SECONDS`, resetting that
global environment variable to `1` second instead of `3`seconds:

```python
@pytest.mark.speed_check
def test_faster(monkeypatch):
    """ Test with monkeypatch of slow GLOBAL_SLEEP_SECS removed """

    monkeypatch.setattr(example, "GLOBAL_SLEEP_SECS", 1)

    answer = example.some_math_function(2, 1)
    assert answer == 6
```

Here we use the `monkeypatch` built-in fixture (more on fixtures later)
as a function argument in our test, allowing us to use `monkeypatch` in the
test. We call `monkeypatch.setattr(OBJECT, "ATTRIBUTE", ATTRIBUTE_VALUE)`
to set the object's `ATTRIBUTE` to `ATTRIBUTE_VALUE`. If we want to
replace a module's global variable with a new one, the `OBJECT` *is* the
module containing the global variable (note we had imported the module `example`
before using it in the test). The second argument is the attribute we want
to replace as a string (ie, in quotation marks) -- in this case, the module's
global variable `GLOBAL_SLEEP_SECONDS` is the attribute we want to be replaced.
Finally, the third argument is the value we want to set the attribute (argument
2) with. Here we are changing that value to `1`. Now the test will run with
a 1-second sleep instead of its original 3-second sleep. After the test is
over, all objects changed by `monkeypatch` revert to their original values.

### Mock a function with a replacement function

It might be necessary to replace a function (or class method) that is called
in the course of your test with a simpler function. In this next example,
we're going to replace two class methods with replacement methods. Recall
in our `example.py` module, `slow`, sleeps for a set amount of time and
`multiply` multiplies two numbers together. Here's how we can replace
those methods with new methods:

```python
@pytest.mark.speed_check
def test_mocked_functions(monkeypatch):
    """ Test monkeypatch replacing a function with a different function """

    def fake_multiply(_self, _first, _second):
        """ Output 2 regardless of input """
        return 2

    monkeypatch.setattr(example.Math, "slow", lambda _: None)
    monkeypatch.setattr(example.Math, "multiply", fake_multiply)

    answer = example.some_math_function(2, 1)
    assert answer == 2
```

Like in the above example, `monkeypatch` is a function argument of our test,
allowing us to use the `monkeypatch` fixture as an object in our test. We want
to replace the `slow` function with a fast function that does *nothing* when
called. To use monkeypatch that function recall we use
`monkeypatch.setattr(OBJECT, "ATTRIBUTE", ATTRIBUTE_VALUE)`. In this case, the
`OBJECT` is the `example.py` module's `Math` class. The `ATTRIBUTE` to be
replaced is the `slow` method (in quotation marks). For the third argument,
we replace the `slow` method with a *lambda function* (an inline,
nameless function). This lambda function will receive the same arguments
as the real function would send. In our case, it will receive one argument which
we don't care about so we replace it with `_` (although if you're interested,
the argument passed during the test is the class's `self` object). The lambda
function returns `None`. This means that `time.sleep(GLOBAL_SLEEP_SECS)`
is no longer called by `Math.slow`, so the test should run almost instantly.

The `multiply` method could also be replaced with a *lambda function*, but
here we'll show how to replace it with a named function. First, we create
the replacement function inside the test. The replacement function here is
`fake_multiply` and it will receive three arguments. I labeled those arguments
with leading underscores to indicate they won't be used by our mocked function
(note, however, if we wanted to, we *could* use those variables in the mocked
function). The function simply returns `2` no matter what input it receives.
We `monkeypatch` replace the `multiply` method the same way we replaced the
`slow` method, using `fake_multiply` as the replacement
function (third argument). When the test runs, both monkeypatched class
methods are replaced with their mocked functions.

### Set or remove an environment variable for a test

If environment variables are important to your code, you may want to manipulate
environment variables as part of your tests. Introducing `monkeypatch.delenv`
and `monkeypatch.setenv`. Let's take a look at an example. This is the
function we are testing in `example.py`:

```python
def environment_var_function():
    """ Some function that deals with environment variables """
    if os.environ.get("MY_VAR") == "true":
        return "MY_VAR is set to 'true'"
    else:
        return "MY_VAR is not set to 'true'"
```

The test we are using looks like this:

```python
def test_alter_environment_variable(monkeypatch):
    """ Test with monkeypatch setting an environment variable """

    # If raising=True (default) will raise error if MY_VAR doesn't exist
    monkeypatch.delenv("MY_VAR", raising=False)

    assert example.environment_var_function() == "MY_VAR is not set to 'true'"

    monkeypatch.setenv("MY_VAR", "true")

    assert example.environment_var_function() == "MY_VAR is set to 'true'"
```

As in previous examples, the `monkeypatch` fixture is an argument for our function.
The important environment variable for this function is `MY_VAR`. First,
we remove the environment variable in case it is already set to something
with `monkeypatch.delenv("MY_VAR", raising=False)`. Note, as the comment
explains, if `raising` is set to True (default), pytest will raise an error
if `MY_VAR` was not already set. Later in the test, we set `MY_VAR` to our
desired value `"true"`, using `monkeypatch.setenv("MY_VAR", "true")`.
After the test concludes, the environment variable will be reverted to
the value it had before the test ran.

## 4. `tmp_path` and `importlib`

Sometimes you will test code that writes to files. Testing
this type of code can be difficult, as you want all of *your* files to be
the same before and after your tests run. `importlib` and `tmp_path`
come in clutch for this type of test.

Here's an example function we'll want to test from `example.py`:

```python
def update_file_via_pathlib(path):
    """ Get the contents of an input pathlib file object """
    contents = path.read_text()
    new_contents = "Check this out: " + contents.strip() + " BAM!"
    path.write_text(new_contents)
    return new_contents
```

This function reads a file, then re-writes the file with updated text
before and after the file. To test the functionality let's say we have
a long, complicated test file named `infile.txt` under a separate directory in
our project called `test_data`. (Note: for this example, the actual file text
just reads "Awesome test data!"). We want to make sure our test can update
`infile.txt`, but we don't want that file to change every time the test
runs. Here's a test that does just that:

```python
import importlib
...

def test_update_file_pathlib(tmp_path):
    """ Test the update_file_pathlib function """
    # Establish path to a temporary file under a temporary directory
    test_file = tmp_path.joinpath("testfile.txt")

    # Get the file contents of a file in our test_data directory
    with importlib.resources.path(
        "pytest_examples.test_data", "infile.txt"
    ) as test_path_og:
        # Write data from our test_data directory file to the temporary file
        test_file.write_text(test_path_og.read_text())

    example.update_file_via_pathlib(test_file)
    assert test_file.read_text() == "Check this out: Awesome test data! BAM!"
```

Let's break down what's happening in this test. First `tmp_path` is a
`fixture` object (like `monkeypatch` - more on fixtures later) that is
a function argument for our test. The `tmp_path` fixture creates a
temporary directory (that will be deleted after the test ends) and returns
a [pathlib.Path](https://docs.python.org/3/library/pathlib.html){: target="_blank", rel="noopener noreferrer" }
object for that temporary directory. With `test_file = tmp_path.joinpath("testfile.txt")`
we point to a temporary file in the temporary directory. Next

```python
    with importlib.resources.path(
        "pytest_examples.test_data", "infile.txt"
    ) as test_path_og:
        test_file.write_text(test_path_og.read_text())
```

This `with` context block imports our test file (`infile.txt`) from our
test directory as a `pathlib.Path` object. Note the file structure when
using importlib:

```text
pytest_examples/
├── __init__.py
|
├── src/
|   ├── __init__.py
|   ├── example_test.py
|   └── example.py
|
├── test_data/
|   ├── __init__.py
|   └── infile.txt
```

Each directory (including the base project directory) must be treated as a
`package`, meaning it must contain an `__init__.py` file for
`importlib` to see the file your want it to see. The arguments are
`importlib.resources.path("PACKAGE", "FILE")`. Then with the line
`test_file.write_text(test_path_og.read_text())` we are writing the contents
of our test `infile.txt` to our temporary file `testfile.txt` in our
temporary directory. We then proceed to alter our test file using our
function we are testing `update_file_via_pathlib(PATH)`. The *temporary*
file is updated instead of our permanent `test_data/infile.txt` file, and
we can test the update was successful. The temporary file will be deleted
after the test concludes.

## 5. `fixture`s and the `conftest.py` file

Sometimes in your tests, you will need an action performed before (and possibly
after) a test is run. A common action is creating and then deleting a resource
like a database. This is called **setup** and **teardown**. In `pytest`,
this functionality is best achieved through `fixtures`. Fixtures are
simply functions that are used as arguments to your test that do something,
return an object to use during the test, and then possibly do something else
after the test completes. We've already used `fixtures` in this article.
`monkeypatch` and `tmp_path` are built-in fixtures (ie fixtures in `pytest`'s
code). Creating your own *custom* fixtures is very easy. Just write a
function that is visible to your test, mark the function as a `fixture`,
and then insert that function as an argument to your test.
Let's look at an example:

```python
import random
import pytest
...

@pytest.fixture
def speedup(monkeypatch):  # Notice I pass a fixture (monkeypatch) to another fixture
    """ Fixture to speed up tests by fixing GLOBAL_SLEEP_SECS """
    sleep_time = random.randint(1, 10) / 50
    monkeypatch.setattr(example, "GLOBAL_SLEEP_SECS", sleep_time)
    return sleep_time


def test_with_speedup(speedup):
    """ Use local fixture in test """
    answer = example.some_math_function(2, 1)
    assert answer == 6
```

The function `speedup` is a fixture because it is decorated with
`@pytest.fixture`. Note that fixtures can call on other fixtures, so in
this example, `speedup` calls on the built-in fixture `monkeypatch`.
It then uses monkeypatch to change the value of `GLOBAL_SLEEP_SECONDS` to
a short random number between `.02` and `.2`. and returns `GLOBAL_SLEEP_SECONDS`
new value. Our test `test_with_speedup` uses the local fixture `speedup`
(local, meaning in the same module). The result is the test runs much
faster after altering the `GLOBAL_SLEEP_SECONDS` global variable.

The fixture can also be stored in a centralized location so lots of different
test files can see the same fixture. To do this, store your fixtures in
a file named `conftest.py`, either in the same folder as your tests, or
in a parent folder of the tests. Then just treat that `fixture` as if it
were a local `fixture` in the same file as your test. Let's see an example
of how this works:

In `conftest.py`:

```python
@pytest.fixture(autouse=True)
def time_test():
    """ Time a test and print out how long it took """
    before = time.time()
    yield
    after = time.time()
    print(f"Test took {after - before:.02f} seconds!")


@pytest.fixture(autouse=True, scope="session")
def time_all_tests():
    """ Time a test and print out how long it took """
    before = time.time()
    yield
    after = time.time()
    print(f"Total test time: {after - before:.02f} seconds!")
```

In `example_test.py`:

```python
@pytest.mark.speed_check
def test_basic():
    """ Test main without any changes """
    answer = example.some_math_function(2, 1)
    assert answer == 6
```

Here we introduce several new facts about `fixtures`. First, the
`@pytest.fixture` decorator can take arguments. Here we pass `autouse=True`.
This makes it so tests will automatically use the fixtures `time_test`
and `time_all_tests` which use `autouse=True`. If we didn't set `autouse=True`,
we would have to call the fixtures for every test that wanted to use them
by providing them as function parameters (like `speedup` above).

Next, fixtures can be scoped.
By default a fixture will use `scope="function"`, and the fixture will
run for every function that calls it. `time_test` will run for every function,
even without being explicitly called because
it is set to `autouse=True` and to the default `scope="function"`.
`time_all_tests` will run only once because it set `scope="session"`, meaning
once per testing session. The final new idea introduced here is using, `yield`
in our fixtures. If `yield` is used instead of `return`, your fixture will first
perform its setup. It will then yield some value (in our case nothing -- or
`None` -- is yielded, but any object *can* be yielded to the test). Finally,
after the test is run (or all the tests are finished running if the
`scope="session"`) the code after the `yield` statement will run
(ie, the teardown).

Therefore in our example, `time_test` will get the time
before every test, `yield` to the test run, get the time after each test,
and then print the difference between those times (ie how long the test took
to run). Likewise, `time_all_tests` will get the time before the first test is
run, `yield` to *all* the tests, get the time after the last test has run,
and report the difference (ie, the time it took for all the tests to run).

## 6. Testing python exceptions

Your code might generate exceptions, either intentionally with `raises ERROR`,
or unintentionally with an error raised by a dependent library or the standard
library. To test exceptions in your code, use a `with pytest.raises(ERROR)`
context block. Let's see an example:

In `example.py`:

```python
def error_function(raise_error):
    """ Function will raise an error if you'd like it to """
    if raise_error:
        raise RuntimeError("Alas, there is an error!")
    return True
```

In `example_test.py`:

```python
import pytest
...
def test_error_raising():
    """ Test that use pytest.raises to check for errors """
    with pytest.raises(RuntimeError):
        example.error_function(True)

    with pytest.raises(RuntimeError, match="Alas, there is an error!"):
        example.error_function(True)

    with pytest.raises(RuntimeError, match="Alas.*there.*error!"):
        example.error_function(True)

    assert example.error_function(False) is True
```

We use `with pytest.raises(RuntimeError):` to tell pytest "we expect this
block of code to raise a `RuntimeError`. If a `RuntimeError` error is raised,
the test continues. If a `RuntimeError` is not raised, the test will fail
with an exception message `Failed: DID NOT RAISE <class 'RuntimeError'>`.
In this way, you ensure an error is raised where expected. For even more
control you can ensure that the error message matches what you expect.
To do so use `with pytest.raises(ERROR, matches=MATCHES)`, where matches
is a regex style string matching the expected error message.

## 7. Checking stdout and log messages

Your code may write messages out to a `log`, or it might `print()` messages
to `std_out` or `std_error`. You might want to test that those messages are
*actually* `logging` or `print`ing as you expected. To test for those messages
we need two new built-in `fixtures` -- `caplog` and `capsys`. For example,
tests using `caplog` and `capsys` recall that the file we are testing,
`example.py` has a function `some_math_function` with these lines of
code:

```python
    ...
    if after - before > 2:
        LOGGER.warning("warning message!")
        LOGGER.info("info message!")
        print("print message")
```

We will write tests to make sure those lines of code are reached if
the function takes more than `2` seconds before reaching that point.

### Use `caplog` to test for log messages

With the `caplog` built-in fixture, we can test for log messages in our code.
Let's look at an example:

```python
@pytest.mark.output_capturing
def test_caplog_standard(caplog):
    """ Use caplog to test logging messages (at standard WARNING level) """
    answer = example.some_math_function(2, 1)
    assert answer == 6
    assert "warning message!" in caplog.text
    assert "info message!" not in caplog.text
```

To use the `caplog` built-in fixture, we use `caplog` as an argument to our
test function (just like we do with any other fixture). `caplog` then captures
logging output to itself (rather than a log file or wherever it was being
written to before). To see the contents of the captured log output,
we can use `caplog.text`. Note in the example, the log `info` message
was not captured. This is because by default loggers capture `warning`
level and above messages. To capture an `info` level message, we can make the
caplog fixture temporarily alter our logger to report `info` level messages, like so:

In `example_test.py`:

```python
@pytest.mark.output_capturing
def test_caplog_debug(caplog):
    """Use caplog to test logging messages (at debug level)"""
    caplog.set_level(logging.DEBUG)
    answer = example.some_math_function(2, 1)
    assert answer == 6
    assert "warning message!" in caplog.text
    assert "info message!" in caplog.text
```

### Use `capsys` to test for `stdout` and `stderr` messages

Now we want to capture the line `print("print message")` from `example.py`.
This message is sent to `stdout`. We can capture messages sent to `stdout`
(like print messages) with `capsys`. That looks like so:

```python
@pytest.mark.output_capturing
def test_capsys(capsys):
    """ Use caplog to test print messages"""
    answer = example.some_math_function(2, 1)
    assert answer == 6
    captured = capsys.readouterr()  # Note this resets the internal buffer
    assert "print message" in captured.out
```

Just like with `caplog`, `capsys` is a built-in fixture that we use as
an argument to our test function. It then captures all messages sent
to `stdout` and `stderr` to itself instead of the terminal. To read
messages in `capsys` captured internal buffer call `capsys.readouterr()`.
This resets the buffer and returns what was in the buffer up until that
point. Here we set the contents of the buffer to an object, `captured`.
To see what was in that `captured` output, use `captured.out`.

## 8. Parameterizing tests

It is often useful to test a function with many different sets of input
parameters. You could do this all in one test by testing one set of
parameters, asserting the output, testing the next, asserting the next output,
etc. But it is a better practice to keep your tests as short as possible,
with some developers suggesting limiting to **one** `assert` statement if
possible. While I think the **one** `assert` statement requirement is
a bit extreme, we can reduce our `assert` statement count considerably with
these types of tests by **parameterizing**. What does that look like?
Let's see an example.

In `example_test.py`:

```python
import pytest
...

PARAMS = [
    (2, 1, 6),
    (7, 3, 20),
    pytest.param(25, 5, 150, id="large"),
    pytest.param(-5, -3, -8, id="with_negatives"),
]

@pytest.mark.parametrize("first, second, expected", PARAMS)
def test_param_standard(speedup, first, second, expected):
    """ Test function with standard params """
    answer = example.some_math_function(first, second)
    assert answer == expected
```

What we do here is decorate our test function with
`@pytest.mark.parametrize("PARAM VARIABLES", ITERABLE_OF_ITERABLES)`. The `"PARAM VARIABLES"`
is a string of comma-separated variable names to use in your test.
The values for these variables will be filled by an iterable (a `tuple`,
`list`, `generator`, etc.) that will expand to the exact number of variables
you specified in `"PARAM VARIABLES"`. In the example, our variables are
`first`, `second`, and `expected` (3 variables). So each iterable must have 3
pieces. See the first iterable is a tuple `(2, 1, 6)`. Since our input
`ITERABLE_OF_ITERABLES` contains 4 iterables, this test will run 4 times,
each time expanding the contained iterable to the parameters `first`,
`second`, and `expected` for our test. The first time the test runs `first == 2`,
`second == 1`, `expected == 6`. The second time the test runs `first == 7`,
`second == 3`, `expected == 20`.

If the test is run normally, we'll see 4 `.`, one for each passed variant of the test.
If it is run in **verbose** mode, pytest will try to name the tests with something that
makes sense, for the first test appending `[2-1-6]` to the test name. If we
want the **verbose** mode name to be more descriptive, we can use
`pytest.param(ARGUMENTS, id=ID)`. So for our third parametrized test run,
the numbers `(25, 5, 150)` are sent to pytest as `first`, `second`, `expected`,
but the test is named "large", in verbose mode. The resulting output looks
like this:

```text
src/example_test.py::test_param_standard[2-1-6] PASSED
src/example_test.py::test_param_standard[7-3-20] PASSED
src/example_test.py::test_param_standard[large] PASSED
src/example_test.py::test_param_standard[with_negatives] PASSED
```

Another thing you can do with parametrized testing is test two or more
sets of parameters alongside one another. If a test is decorated with
`@pytest.mark.parametrize` multiple times, pytest will run every combination
of those parameters. Let's see this with another example:

```python
import pytest
...
PARAMS = [
    (2, 1, 6),
    (7, 3, 20),
    pytest.param(25, 5, 150, id="large"),
    pytest.param(-5, -3, -8, id="with_negatives"),
]
...

@pytest.mark.parametrization
@pytest.mark.parametrize("first, second, expected", PARAMS)
@pytest.mark.parametrize("half", (True, False))
def test_param_multiple_sets(speedup, first, second, expected, half):
    """ Test 2 sets of parameters """
    answer = example.some_math_function(first, second, half=half)
    if half:
        assert answer == expected / 2
    else:
        assert answer == expected
```

Here, the test is nearly the same as above, except a second
`@pytest.mark.parametrize` decorator is tact on with an new parameter `half`,
with the possible values of `True` or `False`. Pytest will use every
combination of the 4 sets of parameters from the top `parameterize` with the
2 parameters from the bottom `parameterize` for a total of 2x4=8 (eight)
tests run. Once again, pytest will try to name the tests in a way it thinks
makes sense. The verbose output of that run looks like so:

```text
src/example_test.py::test_param_multiple_sets[True-2-1-6] PASSED
src/example_test.py::test_param_multiple_sets[True-7-3-20] PASSED
src/example_test.py::test_param_multiple_sets[True-large] PASSED
src/example_test.py::test_param_multiple_sets[True-with_negatives] PASSED
src/example_test.py::test_param_multiple_sets[False-2-1-6] PASSED
src/example_test.py::test_param_multiple_sets[False-7-3-20] PASSED
src/example_test.py::test_param_multiple_sets[False-large] PASSED
src/example_test.py::test_param_multiple_sets[False-with_negatives] PASSED
```

## 9. Using pytest-cov

It is important to know how much of your codebase is covered by tests, and
specifically, it is important to know which lines of your codebase are
run by tests, and which lines are not run. Pytest has a great tool for this
called `pytest-cov` (which uses `coverage.py` under the hood). To use
`pytest-cov`, first `pip install pytest-cov`. Then run your tests like normal
with a couple of extra command-line arguments. A standard run with `pytest-cov`
looks like `pytest --cov=CODE_TO_CHECK_COVERAGE`. So if I wanted to see how
much of my `src` directory was covered by tests I'd run `pytest --cov=src`.
`pytest-cov` will track which lines of code were run and send that information
to `std_out` like so:

```text
----------- coverage: platform linux, python 3.8.5-final-0 -----------
Name                  Stmts   Miss  Cover
-----------------------------------------
src/__init__.py           0      0   100%
src/conftest.py          22      0   100%
src/example.py           50      1    98%
src/example_test.py     106      3    97%
-----------------------------------------
TOTAL                   178      4    98%
```

This output is useful, but we don't see specifically which lines in
`src/example.py` were covered by our tests and which lines were missed.
For a more detailed, interactive output use the argument `--cov-report=html`.
When this command-line argument is added, an `htmlcov` directory appears in
the directory the tests were run from. This `htmlcov` directory contains
a bunch of `HTML`, `JS`, `CSS`, etc. files that create an interactive
website for viewing code coverage.

If you have a tool like `VS code` extension
`open in browser`, you can right-click `htmlcov/index.html` and select
"open in Default browser" to view the website. The index page shows
coverage like the above `std_out` report. If you then click on `src/example.py`
though, you are brought to a page showing `src/example.py` source code,
highlighted **green** when lines are *covered* and **red** where lines
are *un-covered*.

If there is a line or block of code (like an `if` statement) that you want
`pytest-cov` to ignore in its coverage calculations, then comment that line
or block of code with `#pragma: no cover`. Those lines will then be marked
as `excluded` rather than `missing`, and they won't count toward the percentage
of lines covered vs uncovered.

## Conclusions

Those are my top 9 tips and tricks for using pytest to the fullest. If you
have any others you think I missed, I'd love to hear about them in the
comments. Looking for more information about testing with pytest? I recommend
reading through [pytests thorough documentation](https://docs.pytest.org/en/stable/){: target="_blank", rel="noopener noreferrer" }
for yourself. For another awesome and much more thorough guide to these pytest
features and many more, I highly recommend the book
[Python Testing with pytest: Simple, Rapid, Effective, and Scalable](https://www.amazon.com/Python-Testing-pytest-Effective-Scalable/dp/1680502409){: target="_blank", rel="noopener noreferrer" }
by Brian Okken. Happy testing!
