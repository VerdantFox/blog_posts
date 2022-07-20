# End-to-end webpage testing with Playwright

tags: testing, pytest, python, web

## Introduction

PLAYWRIGHT_LOGO_PIC

We all know testing your code is important, right? Automated tests can give you peace of mind that your code is working as expected and that it continues to work as expected, even as you refactor it. Python has the [pytest](https://docs.pytest.org/){: target="_blank", rel="noopener noreferrer" } framework that gives great tools for testing your python code. You can check out my blog post [9 pytest tips and tricks to take your tests to the next level](/blog/view/9-pytest-tips-and-tricks-to-take-your-tests-to-the-next-level){: target="_blank", rel="noopener noreferrer" } to get yourself jump started testing in python. Javascript has several libraries to test your front-end code. But in website testing, how can we write automated tests to ensure that our back-end code (be it python or something else) is working with our front-end code (javascript, HTML, and CSS).

Introducing [Playwright](https://playwright.dev/python/), a fast, easy-to-use, and powerful end-to-end testing framework. This framework has tools that allow you to write tests that act similar to an actual website user. And playwright has API endpoints in javascript, java, .NET, and **python**! Sound useful? Read on as we use Playwright with python and pytest to write end-to-end tests for our [Connect 4 game](connect-4 url).

## Getting started (installation)

For this blog post we are going to be using the **python** Playwright API. We'll install Playwright with `pip` and we'll interact with and write tests for Playwright in python. I wrote the tests with `python 3.10`, but I believe the tests will work in python version as low as `3.8`. Whatever Python version you are using, I recommend installing Playwright in a [virtual environment](https://realpython.com/python-virtual-environments-a-primer/). Once your virtual environment is activated, to install playwright and the `pytest-playwright-visual` plugin which aides in comparing Playwright snapshots, just run these 4 commands:

```bash
# Upgrade to latest pip
pip install --upgrade pip
# Installs the playwright package and pytest plugin
pip install playwright
# This step downloads and installs browser binaries for Chromium, Firefox and WebKit
playwright install
# Installs a 3rd party pytest plugin for saving and comparing playwright screenshots
pip install pytest-playwright-visual
```

## Auto-generating Playwright code

One really cool feature of Playwright is the command `playwright codegen URL` where `URL` is the URL you want to start generating Playwright commands from. Let's try it out with my VerdantFox Connect 4 game. Assuming you've completed the above [installation](#installation) steps, run the following command:

```bash
playwright codegen https://verdantfox.com/games/connect-4
```

This opens up 2 windows. The first is a chromium incognito browser at <https://verdantfox.com/games/connect-4>{: target="_blank", rel="noopener noreferrer" }. This window is connected to the second window which has a couple buttons at the top and notepad-like display with python code. The code is a python script for opening this web page with Playwright, and then closing the web page and browser. It looks like this:

```python
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://verdantfox.com/games/connect-4
    page.goto("https://verdantfox.com/games/connect-4")

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)

```

As we interact with the first window opened to our website, the second window will record the corresponding Playwright python code to automate replication of those website interactions. Let's test this out. **Click** the bottom-middle circle on the Connect 4 game board. We see the 🔴 red chip fall, followed by the 🔵 blue chip in the same column like normal. In the second window, the following code was added after `page.goto("https://verdantfox.com/games/connect-4")`:

```python
    # Click #circle-3-5
    page.locator("#circle-3-5").click()
```

The end product looks like this:

```python
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://verdantfox.com/games/connect-4
    page.goto("https://verdantfox.com/games/connect-4")

    # Click #circle-3-5
    page.locator("#circle-3-5").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
```

Now lets copy the code from the second window and paste it into a python file (perhaps called `my_playwright.py`). If we run the resulting python file as a script with `python my_playwright.py`, we see a browser window open and then close pretty fast. It did the same things we did to generate the script, but it did them very fast and then closed. To slow the script down so we can the click and the resulting falling 🔴 red and 🔵 blue chips, we can pass in one extra argument to the line that says `browser = playwright.chromium.launch(headless=False)`. Let's change this line to the following:

```python
browser = playwright.chromium.launch(headless=False, slow_mo=1000)
```

This extra argument `slow_mo=1000` tells the playwright runner to wait 1000 milliseconds (1 second) in between each action. Now if we re-run the script, we'll see the browser open and then we'll see the falling 🔴 red and 🔵 blue chips before the browser closes.

This is awesome! Now we have a means to quickly write playwright scripts that can automate actions for us. Such scripts could be useful on their own. For instance you could write a script that runs once an hour that opens up a website, logs in, and polls the page for information. But beyond that, we have a means of quickly finding playwright commands for writing automated tests, without having to dig through documentation and without having to read through the webpage's DOM (Document Object Model) ourself.

## Understanding the pieces

Now that we have seen how to quickly generate a Playwright script with the `playwright codegen` command, let's dig a little deeper into that code that was auto-generated, along with a couple other key concepts not included in that auto-generated script.

### Browser

The `browser` object handles the browser that is opened to run Playwright commands. The documentation for the `browser` object can be found [here](https://playwright.dev/python/docs/api/class-browser){: target="_blank", rel="noopener noreferrer" }. Playwright can open a browser for Chromium (the base for browsers like chrome, edge and brave), WebKit (the base of iOS browser for applications like Safari), or Firefox. When writing a script you would launch a browser with something like:

```python
browser = playwright.firefox.launch()
```

There are a few arguments that can be passed to `browser.launch()` that help define the experience of working with the browser. The most important two to learn are `headless` and `slow_mo`.

#### headless

```python
playwright.chromium.launch(headless=False)
```

By default `headless` is set to `True`. This means that the browser is launched in `headless` mode. In headless mode, the browser doesn't open visibly but behind the scenes. Oftentimes this is good. For instance, when running tests in CI there will be no screen to look at, so not visibly showing the browser makes sense and is faster. However, when we are developing Playwright scripts or tests, generally we want to *see* what the script or test is doing. In this case we will pass `headless=False` to the `browser.launch()` code.

#### slow_mo

```python
playwright.webkit.launch(headless=False, slow_mo=1000)
```

We mentioned this one briefely above when talking about [playwright codegen](#auto-generating-playwright-code). By default, actions in a Playwright script or test will proceed one after the other without pause. This means playwright can run said scripts/tests quite fast -- sometimes too fast to see what is actually happening. While developing, you might want to slow things down so you can actually see the actions being performed. To do so pass the `slow_mo=MILLISECONDS` argument to `browser.launch()`. Then all subsequent actions called against elements of the webpage will have a delay of `MILLISECONDS` between each action (e.g. `browser.launch(slow_mo=500` will have a 0.5 second delay between each action). Coupling this with `headless=False` means we can clearly follow what the script/test is doing.

### Context

A browser's `context` provides a way to operate multiple independent browser sessions. A new context can be thought of like an "incognito" window. Each new context shares no session, cookies, history, etc. with other browser `context` objects. In a script, we call `browser.new_context()` to generate the new incognito window. Getting a new browser and browser context would look like this:

```python
browser = playwright.chromium.launch(headless=False)
context = browser.new_context()
```

The full documentation for the browser `context` can be found [here](https://playwright.dev/python/docs/api/class-browsercontext){: target="_blank", rel="noopener noreferrer" }.

### Page

The `page` object provides methods to interact with a single tab in a browser. It is spawned from a browser context with `context.new_page()`. A `browser` can have multiple `context`s and a `context` can have multiple `page`s. Here are some important methods that we can call from a `page`. A full list of interactions can be found [here](https://playwright.dev/python/docs/api/class-page){: target="_blank", rel="noopener noreferrer" }.

#### page.goto(url, **kwargs)

We can use `page.goto(URL)` to open a new browser tab at the provided URL. In our example from earlier `page.goto("https://verdantfox.com/games/connect-4")` opened a tab to the VerdantFox Connect 4 game.

#### page.screenshot()

`page.screenshot()` takes a screenshot of the visible page.

#### page element interactions

Many interactions can be called from a `page` object. For instance we can call `page.click(selector)` to mouse-click an object identified by a **selector** (more on **selectors** later). Other `page` object interactions include `page.check(selector)` to check a checkbox or radio button, `page.hover(selector)` to hover over an object, and many others.

#### page.locator(selector)

The `page.locator(selector)` method returns an element locator, identified by a **selector** that can be used to perform actions on the page. More on locators and selectors next. I tend to prefer performing actions on these locators rather than on the `page` object directly.

### Locators

According to the [locators documentation](https://playwright.dev/python/docs/api/class-locator){: target="_blank", rel="noopener noreferrer" }:

> Locators are the central piece of Playwright's auto-waiting and retry-ability. In a nutshell, locators represent a way to find element(s) on the page at any moment. Locator can be created with the page.locator(selector, **kwargs) method.

Locators have a plethora of interactive functions that can be called off of them mirrored by the [page element interactions](#page-element-interactions). These include things like `locator.click()` to mouse-click the element on the page represented by the `locator`, `locator.check()` to check a checkbox or radio button, or `locator.fill(value)` to fill an `<input>` or `<textarea>` element. There's even `locator.screenshot()` to take a screenshot of a specific element on the page.

Locators have a variety of `is_something()` methods that return a boolean. For instance `locator.is_checked()` returns `True` if the represented element is a checkbox that is checked, `locator.is_hidden()` returns `True` if the represented element is hidden on the page, and `locator.is_disabled()` returns `True` if the represented object is disabled.

A given locator can represent one **or more** elements. A locator represents multiple elements if its `selector` applies to multiple elements. You can call `locator.count()` to get a count of how many elements the locator applies to. In a case where a locator applies to multiple elements, a call like `locator.click()` would raise an error, since a `locator.click()` must apply to only **one** element. There are methods to get one element out of the many represented by the locator. `locator.first` gets the first element represented by the locator, `locator.last` gets the last element represented by the locator, and `locator.nth(index)` gets the `nth` element represented by the locator where `index` passed is `0` based (so `locator.nth(0)` gets the first element).

Locators can be chained off of one another to narrow down to a more specific locator with `locator.locator(selector)`. For instance, you could call `page.locator("#introduction").locator("ul").locator("li").nth(3)`. This would first get the element with the "introduction" id, then grab the "ul" (unordered list) child element of the "introduction" element, then the "li" (list item) elements of the list, then grab the 4th (0, 1 ,2 ,3) "li" element in the list.

### selectors

Selectors are strings that are used to create [locators](#locators). There are variety of selector types that are described in the [selector's quick guide documentation](https://playwright.dev/python/docs/selectors#quick-guide){: target="_blank", rel="noopener noreferrer" }. These include text selectors like `page.locator("text=Log in").click()`, CSS selectors like `page.locator("button").click()` and `page.locator("#nav-bar .contact-us-item").click()`, and a variety of other selectors and combinations thereof.

### Expect

Asserting on the expected state of an element in a web application can be tricky to time. Assert too early and the expected state might not have been reached yet due to some javascript delay. Wait too long and you're just wasting time. The `expect` object has methods for creating assertions that retry until the expected condition is met -- or until a timeout is reached. Here's an example from the [documentation on Playwright assertions](https://playwright.dev/python/docs/test-assertions){: target="_blank", rel="noopener noreferrer" }:

```python
from playwright.sync_api import Page, expect

def test_status_becomes_submitted(page: Page) -> None:
    # ..
    page.click("#submit-button")
    expect(page.locator(".status")).to_have_text("Submitted")
```

> Playwright will be re-testing the node with the selector .status until fetched Node has the "Submitted" text. It will be re-fetching the node and checking it over and over, until the condition is met or until the timeout is reached. You can pass this timeout as an option.

There are a ton assertion methods that can be called on an `expect` object including `expect(locator).to_have_text(expected, **kwargs)`,  `expect(locator).to_have_css(name, value, **kwargs)`, `expect(locator).to_have_class(expected, **kwargs)` and a variety of others including the inverses of all of these (e.g. `expect(locator).not_to_have_text(expected, **kwargs)`).

## Playwright and pytest

Cool, we've got a Playwright script and we understand some of the basic building blocks of Playwright. How can we take what we've learned creating such a script, and convert it into automated tests for our website? Introducing the `playwright-pytest` plugin. Here we'll discuss `pytest-playwright` CLI flags, playwright fixtures, the `pytest-playwright-visual` plugin, and the playwright debugger, all in the context of a working test I wrote against the [VerdantFox Connect 4 game](https://verdantfox.com/games/connect-4){: target="_blank", rel="noopener noreferrer" }. The test mirrors our simple code we generated earlier with [playwright codegen above](#auto-generating-playwright-code). We'll call the test file `test_connect_4` for future CLI discussions. Here is the file with our one test:

`test_connect_4`

```python
import re
from typing import Callable

from playwright.sync_api import Locator, Page, expect


def test_single_move(page: Page, assert_snapshot: Callable) -> None:
    """Test that a single move by human, followed by AI behaves as expected"""
    page.goto("https://verdantfox.com/games/connect-4")
    page.locator("#circle-3-5").click()
    expect(page.locator("#circle-3-5")).to_have_class(re.compile(r"color-red"))
    expect(page.locator("#circle-3-5")).to_have_css(
        "background-color", "rgb(255, 0, 0)"
    )
    expect(page.locator("#circle-3-4")).to_have_class(re.compile(r"color-blue"))
    expect(page.locator("#circle-3-4")).to_have_css(
        "background-color", "rgb(0, 0, 255)"
    )
    assert_snapshot(page.locator("#board").screenshot())
```

### Useful CLI flags

Before we dive into the contents of the above test, lets talk about useful CLI flags you can use when running pytests with the `pytest-playwright` plugin. A full list of `pytest-playwright` CLI arguments can be found [here](https://playwright.dev/python/docs/test-runners#cli-arguments){: target="_blank", rel="noopener noreferrer" }.

#### `--browser=BROWSER`

As we'll soon see in our discussion of fixtures, with pytests we usually don't work directly with the `browser` object. As such we won't use `playwright.chromium`, `playwright.webkit` or `playwright.firefox`. The `playwright-pytest` plugin appears to default to running tests against the `playwright.chromium` browser. To actively choose a browser to run all tests against, you could run `pytest test_connect_4 --browser=firefox` or `--browser=webkit` or `--browser=chromium`. You can even pass multiple flags to run against multiple browsers. For instance `pytest test_connect_4 --browser=firefox --browser=webkit --browser=chromium` will run the test `test_single_move` 3 times back-to-back, one with each browser.

#### `--headed` and `--slowmo=MS`

Because we don't usually work with the browser in tests, we do not call `browser.launch()`. If you recall from the earlier [section on the `browser` object](#browser), the `.launch()` method takes some useful methods: `headless=BOOL` which allowed us to run in "headed" mode to watch our tests run and `slow_mo=MS` to add a wait period between each command. To provide this functionality with pytests, we can pass the `--headed` flag which runs all Playwright tests in "headed" mode (as opposed to "headless" mode), and we can pass `--slowmo=MS` to add a wait period of MS milliseconds between each playwright command.

#### `--screenshot=WHEN` and `--video=WHEN`

When a playwright test fails, the easiest way to learn *why* it failed is to visually *see* what the browser state looks like at the time of the test failure. `pytest-playwright` is capable of capturing a screenshot at the end of a test with `--screenshot=WHEN` where `WHEN` can be `on`, `off` or `only-on-failure`. It defaults to `off`, but changing to `--screenshot=only-on-failure` is a nice way to get an image of the browser at the time of failure for failed tests. This can be especially useful for long-running test suites. If a test suite runs for 10 minutes, and 1 test fails in the middle, having that snapshot to look at afterwards can really save a headache. What's even better than a screenshot? A video (sometimes). With `--video=WHEN` `pytest-playwright` can capture a video of the browser during each test. `WHEN` can be set to `off` (default, fastest), `on` (capture a video of each test), and `retain-on-failure` (capture a video for each test, but delete the video if the test passes). If you use this flag, I suggest the `retain-on-failure` version.

### Useful fixtures



### pytest-playwright-visual plugin

### playwright debugger tool


### SNIPPETS PULLED

In pytests, it is possible to deal with the browser directly with the `browser` fixture. This fixture is **session** scoped, meaning one browser is generated at the start of all tests, and it is used for each test. Each test is then separated by a function scoped `context`. More on the `context` object and fixture next. However, in pytests, usually we don't need to deal with the `browser` object directly. Instead, most commonly, we deal with the `page` fixture which calls the `browser` fixture to generate a new `browser` in the background. More on the `page` fixture and object soon. Not creating our own `browser` object means we can't call something like `playwright.firefox`. Instead, when working with pytests, to pick a specific browser we'd supply the command line argument `--browser firefox` (or `chromium` or `webkit`), where `chromium` is the default.
