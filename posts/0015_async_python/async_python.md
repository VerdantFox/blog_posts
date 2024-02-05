# Concurrent python programming with async, threading, and multiprocessing

tags: python, async, threads, multiprocessing, concurrency, parallelism, web scraping

## Introduction

01_INTRO_PIC

One of the best ways to achieve **big** speed improvements in Python code is through concurrency: doing several tasks at the same time. In this post, I briefly describe concurrency in python and give some examples for running code concurrently with "async" functions, "threading", and "multiprocessing".

## Defining key terms

- **Concurrency**: _Making progress on_ multiple programming tasks at the same time. This does not necessarily mean actively executing multiple lines of code at the same time. It often involves sending multiple requests to another executor to work on tasks in parallel and return the results to the main program.
- **Parallelism**: A form of **concurrency** which _does_ mean executing multiple lines of code at the same time. It requires breaking code into smaller chunks and making multiple **CPU cores** execute code simultaneously.
- **CPU (Central Processing Unit) core**: A CPU core executes code, one instruction at a time. Modern computers typically have multiple CPU cores, each able to execute a set of instructions (code) in **parallel** with other CPU cores on the same CPU processor.
- **I/O (Input/Output)**: "Work" performed by external services (other than the running Python code). Broadly, input refers to "reading" incoming data, while "output" refers to writing outgoing data. Examples of I/O include reading/writing to a file or database or sending/receiving network or web requests. If Python code is structured appropriately, Python code can run multiple I/O-bound tasks **concurrently** in the background, while Python bytecode runs in the foreground. Processes that involve **I/O** tasks are said to be **I/O-bound**. This is opposed to process that have no (or limited) **I/O** tasks, which are said to be **CPU-bound**.
- **Thread**: A small unit of code to execute in a process. A process is the overall running instance of a program, and within that process, multiple threads can execute **concurrently**. Each thread represents an independent sequence of instructions that can be scheduled and executed by the operating system. In many languages, **threads** can execute code on multiple **CPU cores** at the same time. A Python program can spawn many threads, but _only one can ever execute Python code simultaneously_ due to the **GIL**. However, while only one thread can _execute Python code_ at once, other threads can "wait" to receive the results of I/O-bound work they had previously kicked off.
- **GIL (Global Interpreter Lock)**: A python implementation detail. The GIL synchronizes access to Python objects by preventing multiple **threads** from executing Python bytecode at once. Because of this, Python is optimized to run very fast on one thread, but cannot execute code on multiple threads simultaneously. This means Python normally only ever runs on _one_ CPU core, even if the machine it runs on has many cores idle.
- **Async/await**: A way to achieve **concurrency** from a single thread in Python. It involves running an **event loop** and converting regular Python functions to `async` functions (or coroutines) with the `async` keyword. The code then `await`s or pauses execution of the code at key places to allow other coroutines or I/O-bound work to run, resuming work later, once the coroutine or I/O bound task completes.
- **event loop**: The **event loop** coordinates asynchronous tasks (or coroutines) in Python (code that uses the `async` and `await` keywords). It is responsible for scheduling, pausing, and resuming code execution, ensuring tasks make progress without blocking execution of the entire program. In python, only _one_ **event loop** can run per thread.
- **coroutine**: In Python, a coroutine often refers interchangeably to two related concepts and I will probably use the two interchangably in this article.
  1. **coroutine function**: A function defined using the `async def` syntax. The `await` keyword can only be used inside a **coroutine function**.
  2. **coroutine object**: An object _returned by_ a **coroutine function**. When an `async def` defined **coroutine function** is called (example: `my_coroutine()`), the code inside does not execute immediately. Instead it must be awaited with the `await` keyword, at which time the code defined in the `async def` function will execute. This second definition of **coroutine** is also often called an **awaitable**.

## Visual Examples

02_SYNC_PIC

With synchronous code, requests are made sequentially, one after the next.

03_ASYNC_PIC

With `async`/`await` code, we split tasks up to run concurrently. We purposefully set `await` steps in our code where we wait for **I/O-bound** work to complete and resume our python code. An **event loop** coordinates waiting tasks, resuming our Python code when background **I/O-bound** work completes. In this paradigm, all Python code runs on a single thread.

04_THREADING_PIC

With **threaded code**, we split tasks up to run concurrently. Unlike with `async`/`await` style code, we do not set specific places to wait for background tasks to complete. Instead, our **CPU coordinates all threads**, alternating which thread executes code at any given time. Because of the **GIL**, only one thread can run Python code at a time (on a single CPU core). However, many threads can wait on **I/O-bound** work to complete in the background while one active thread runs Python code. The CPU alternates the active thread rapidly, sometimes even alternating between the start of one line of Python code and the end of that same line. Thus race conditions in **threaded** code are less predictable than in `async`/`await` code.

05_MULTIPROCESSING_PIC

With **multiprocessing** code in Python, we split tasks up to run in **parallel** on multiple CPU cores. **Each** multiprocess task running on a separate core can execute python code **at the same time**. This can vastly speed up Python code that does not involve **I/O** work such as math-heavy operations. However, muliprocessing involves limitations. I won't go into significant detail on those limitations in this article, but they involve a larger startup overhead and limited communication between processes.

## The code

[The code for this blog article can be found on GitHub here](https://github.com/VerdantFox/async-examples). The code includes the following folders: `web/`, `cpu_bound/`, and `locks/`. Each folder has examples of synchronous code, followed by various examples of code that runs concurrently. The code was written for Python 3.11, but most of the code should work as early as Python version 3.7, and should all work for later versions of Python. You'll need to install the following packages to follow along with the examples:

- [beautifulsoup4](https://beautiful-soup-4.readthedocs.io/en/latest/) (for parsing HTML)
- [rich](https://rich.readthedocs.io/en/latest/introduction.html) (for pretty printing colors)
- [requests](https://requests.readthedocs.io/en/latest/) (for making sync-only HTTP requests)
- [httpx](https://www.python-httpx.org) (for making sync or async HTTP requests)
- [aiohttp](https://docs.aiohttp.org/en/stable/) (for making async-only HTTP requests)

You can install them all with the following command:

```bash
pip install beautifulsoup4 rich requests httpx aiohttp
```

## HTTP requests

One common use case for concurrency is web requests: usually in the form of [API requests](https://en.wikipedia.org/wiki/API) or [web scraping](https://en.wikipedia.org/wiki/Web_scraping). For this section, we'll be web scraping a Pokémon website to get the names of Pokémon, given their Pokédex number. First, I'll show you how to scrape several pages synchronously. Then we'll see how to get massive speedups using `async`/`await` or threading.

### Synchronous example

The most basic example involves synchronous code execution. We request and process the web pages one-at-a-time. Here's an example:

```python
# web/1_sync.py
"""Download the first 20 pokemon synchronously."""
import time

import requests
from bs4 import BeautifulSoup
from rich import print


def main() -> None:
    print("Starting tasks...", flush=True)
    t0 = time.time()
    results = download_pokemon_list()
    total_seconds = time.time() - t0
    print(
        f"\n[bold green]Code run in [cyan]{total_seconds:,.2f}[green] seconds.",
        flush=True,
    )
    print(f"\n{results=}", flush=True)


def download_pokemon_list() -> list[tuple[int, str]]:
    """Download a list of pokemon from 'pokemondb'."""
    return [download_single_pokemon(num) for num in range(1, 21)]


def download_single_pokemon(pokemon_num: int = 1) -> tuple[int, str]:
    """Get a pokemon from 'pokemondb' by its pokedex number."""
    print(
        f"[yellow]Downloading pokemon {pokemon_num:02}... [/yellow]",
        flush=True,
    )
    url = f"https://pokemondb.net/pokedex/{pokemon_num}"
    resp = requests.get(url, allow_redirects=True)
    resp.raise_for_status()
    header = get_h1(resp.text)
    print(
        f"[green]Retrieved [magenta]{pokemon_num:02}={header}",
        flush=True,
    )
    return (pokemon_num, header)


def get_h1(html: str) -> str:
    """Parse the HTML and return the first H1 tag."""
    soup = BeautifulSoup(html, "html.parser")
    return soup.h1.text


if __name__ == "__main__":
    main()
```

Here's terminal output from running that code:

```bash
❯ python web/1_sync.py
Starting tasks...
Downloading pokemon 01...
Retrieved 01=Bulbasaur
Downloading pokemon 02...
Retrieved 02=Ivysaur
Downloading pokemon 03...
Retrieved 03=Venusaur
Downloading pokemon 04...
Retrieved 04=Charmander
Downloading pokemon 05...
Retrieved 05=Charmeleon
Downloading pokemon 06...
Retrieved 06=Charizard
Downloading pokemon 07...
Retrieved 07=Squirtle
Downloading pokemon 08...
Retrieved 08=Wartortle
Downloading pokemon 09...
Retrieved 09=Blastoise
Downloading pokemon 10...
Retrieved 10=Caterpie
Downloading pokemon 11...
Retrieved 11=Metapod
Downloading pokemon 12...
Retrieved 12=Butterfree
Downloading pokemon 13...
Retrieved 13=Weedle
Downloading pokemon 14...
Retrieved 14=Kakuna
Downloading pokemon 15...
Retrieved 15=Beedrill
Downloading pokemon 16...
Retrieved 16=Pidgey
Downloading pokemon 17...
Retrieved 17=Pidgeotto
Downloading pokemon 18...
Retrieved 18=Pidgeot
Downloading pokemon 19...
Retrieved 19=Rattata
Downloading pokemon 20...
Retrieved 20=Raticate

Code run in 4.15 seconds.

results=[(1, 'Bulbasaur'), (2, 'Ivysaur'), (3, 'Venusaur'), (4, 'Charmander'),
(5, 'Charmeleon'), (6, 'Charizard'), (7, 'Squirtle'), (8, 'Wartortle'), (9,
'Blastoise'), (10, 'Caterpie'), (11, 'Metapod'), (12, 'Butterfree'), (13,
'Weedle'), (14, 'Kakuna'), (15, 'Beedrill'), (16, 'Pidgey'), (17, 'Pidgeotto'),
(18, 'Pidgeot'), (19, 'Rattata'), (20, 'Raticate')]
```

And here's a video showing the code executing in real time with color:

05_WEB_SYNC_VIDEO

Notice how the requests run one after another: "Downloading", then "Retrieving", "Downloading", then "Retrieving". First we kick off a request, then we wait for it to come back, then we kick off the next request and wait for it to come back, etc.

In the above code we use [requests](https://requests.readthedocs.io/en/latest/) to request the web pages and [beautiful soup](https://beautiful-soup-4.readthedocs.io/en/latest/) to parse the HTML we get back. We'll also use [rich](https://rich.readthedocs.io/en/latest/introduction.html) to add color to our `print` statements since color can help us visualize the output more easily. `download_pokemon_list` calls `download_single_pokemon` 20X, once for each of the first 20 Pokémon. The requests are made one after another in a list comprehension. Beautiful soup parses the HTML to get the `<h1>` header which corresponds to the Pokémon's name. The code takes `~4-6` seconds to run.

### Async/await example

Async/await is the preferred, modern approach to running web requests in parallel. In this code example, we convert the synchronous code to `async`/`await` asynchronously executed code using [aiohttp](https://docs.aiohttp.org/en/stable/) to make web requests:

```python
# web/2_async_aiohttp.py
"""Download the first 20 pokemon asynchronously using aiohttp."""
import asyncio
import time

import aiohttp
from bs4 import BeautifulSoup
from rich import print


def main() -> None:
    print("Starting tasks...", flush=True)
    t0 = time.time()
    results = asyncio.run(download_pokemon_list())
    total_seconds = time.time() - t0
    print(
        f"\n[bold green]Code run in [cyan]{total_seconds:,.2f}[green] seconds.",
        flush=True,
    )
    print(f"\n{results=}", flush=True)


async def download_pokemon_list() -> list[tuple[int, str]]:
    """Download a list of pokemon from 'pokemondb'."""
    coroutines = [download_single_pokemon(num) for num in range(1, 21)]
    print("Gathering coroutines into tasks...", flush=True)
    tasks = asyncio.gather(*coroutines)
    print("Done gathering tasks. Running + awaiting tasks...", flush=True)
    results = await tasks
    print("Done gathering results.", flush=True)
    return results


async def download_single_pokemon(pokemon_num: int = 1) -> tuple[int, str]:
    """Get a pokemon from 'pokemondb' by its pokedex number."""
    print(
        f"[yellow]Downloading pokemon {pokemon_num:02}... [/yellow]",
        flush=True,
    )
    url = f"https://pokemondb.net/pokedex/{pokemon_num}"
    async with aiohttp.ClientSession() as session, session.get(url) as resp:
        resp.raise_for_status()
        text = await resp.text()
    resp.raise_for_status()
    header = get_h1(text)
    print(
        f"[green]Retrieved [magenta]{pokemon_num:02}={header}",
        flush=True,
    )
    return (pokemon_num, header)


def get_h1(html: str) -> str:
    """Parse the HTML and return the first H1 tag."""
    soup = BeautifulSoup(html, "html.parser")
    return soup.h1.text


if __name__ == "__main__":
    main()
```

Here's terminal output from running that code:

```bash
❯ python web/2_async_aiohttp.py
Starting tasks...
Gathering coroutines into tasks...
Done gathering tasks. Running + awaiting tasks...
Downloading pokemon 01...
Downloading pokemon 02...
Downloading pokemon 03...
Downloading pokemon 04...
Downloading pokemon 05...
Downloading pokemon 06...
Downloading pokemon 07...
Downloading pokemon 08...
Downloading pokemon 09...
Downloading pokemon 10...
Downloading pokemon 11...
Downloading pokemon 12...
Downloading pokemon 13...
Downloading pokemon 14...
Downloading pokemon 15...
Downloading pokemon 16...
Downloading pokemon 17...
Downloading pokemon 18...
Downloading pokemon 19...
Downloading pokemon 20...
Retrieved 09=Blastoise
Retrieved 08=Wartortle
Retrieved 03=Venusaur
Retrieved 07=Squirtle
Retrieved 16=Pidgey
Retrieved 02=Ivysaur
Retrieved 04=Charmander
Retrieved 01=Bulbasaur
Retrieved 19=Rattata
Retrieved 18=Pidgeot
Retrieved 05=Charmeleon
Retrieved 06=Charizard
Retrieved 17=Pidgeotto
Retrieved 15=Beedrill
Retrieved 12=Butterfree
Retrieved 14=Kakuna
Retrieved 11=Metapod
Retrieved 10=Caterpie
Retrieved 13=Weedle
Retrieved 20=Raticate
Done gathering results.

Code run in 1.67 seconds.

results=[(1, 'Bulbasaur'), (2, 'Ivysaur'), (3, 'Venusaur'), (4, 'Charmander'),
(5, 'Charmeleon'), (6, 'Charizard'), (7, 'Squirtle'), (8, 'Wartortle'), (9,
'Blastoise'), (10, 'Caterpie'), (11, 'Metapod'), (12, 'Butterfree'), (13,
'Weedle'), (14, 'Kakuna'), (15, 'Beedrill'), (16, 'Pidgey'), (17, 'Pidgeotto'),
(18, 'Pidgeot'), (19, 'Rattata'), (20, 'Raticate')]
```

And here's a video showing the code executing in real time with color:

06_WEB_ASYNC_VIDEO

Notice how the code kicks off all the "Download" steps first, some time passes, and then all the "Retrieved" responses come back out of order. What code did we change?

First, we changed any function that needs `await` **I/O-bound** work into a **coroutine function** by slapping an `async` to the front of it. `async def download_pokemon_list` becomes our coordinating async **coroutine function** and `async def download_single_pokemon` is an another **coroutine function**.

```python
results = asyncio.run(download_pokemon_list_gather())
```

👆 This line (inside `main`)is how we start our first **coroutine function** from a regular synchronous function. Here's the documentation on `asyncio.run`:

> \[`asyncio.run` executes an async **coroutine function** and returns the results\]. This function runs the passed coroutine, taking care of managing the asyncio event loop, finalizing asynchronous generators, and closing the threadpool. This function cannot be called when another asyncio event loop is running in the same thread... This function always creates a new event loop and closes it at the end. It should be used as a main entry point for asyncio programs, and should ideally only be called once.

To highlight, `asyncio.run` runs a single **coroutine** from a synchronous function and will error if called when an event loop is already running the current thread.

```python
coroutines = [download_single_pokemon(num) for num in range(1, 21)]
```

👆 This line (inside `download_pokemon_list`) creates our list of **coroutine objects** by calling the async **coroutine functions**. The coroutine functions **do not start** when they are called--they simply create the **coroutine objects** that can be run later.

NOTE: **coroutine functions** can be called inside synchronous functions, creating **coroutine objects**. However, they cannot be `await`ed and thus run inside synchronous functions (except with something like `asyncio.run` or some other limited number of methods).

```python
tasks = asyncio.gather(*coroutines)
```

👆 This line (inside `download_pokemon_list`) converts the **coroutine objects** into `asyncio.Task` objects known to the **event loop**. Note that the tasks are _still_ not started at this point.

```python
results = await tasks
```

👆 This line (inside `download_pokemon_list`) finally kicks off all the tasks created by `asyncio.gather` and waits for the results to come back. It stores the results of the completed **coroutine objects** in a list.

```python
async with aiohttp.ClientSession() as session, session.get(url) as resp:
    resp.raise_for_status()
    text = await resp.text()
```

👆 These lines (inside `download_single_pokemon`) convert the synchronous `requests.get` call to an async call and wait for the response. Without this change, we could not wait for multiple **I/O** responses at once in a single thread.

NOTE: these two lines are equivalent:

```python
async with aiohttp.ClientSession() as session, session.get(url) as resp:
    ...

async with aiohttp.ClientSession() as session:
    async with session.get(url) as resp:
        ...
```

### Alternative async/await methods and libraries

Here are a few alterative ways we could have achieved the same goal with `async`/`await`.

#### httpx instead of aiohttp

[Httpx](https://www.python-httpx.org) is an alternative library to [aiohttp](https://docs.aiohttp.org/en/stable/) for making async web requests. It's a popular library, and I like it for a couple reasons.

1. It can make either asynchronous or synchronous web requests. `aiohttp` can only make `async` web requests and `requests` can only make synchronous web requests.
2. Its methods and syntax are nicer to work with than `aiohttp` in my opinion. Working with `httpx` feels nearly identical to working with `requests`, which I like.

However, with testing, I've found that `httpx` requests are significantly slower than `aiohttp`. It doesn't matter much for a small number of requests, but I think the difference adds up over many requests. With this example code, `aiohttp` averages around 1.6 seconds for 20 requests and `httpx` averages around 2.6 seconds for the same number of requests.

Here's the different code for using `aiohttp` vs `httpx` and `requests` one after the other:

```python
import aiohttp
import httpx

# aiohttp (async only)
async with aiohttp.ClientSession() as session, session.get(url) as resp:
    resp.raise_for_status()
    text = await resp.text()

# httpx (async)
async with httpx.AsyncClient() as client:
    resp = await client.get(url, follow_redirects=True)
    resp.raise_for_status()
text = resp.text

# httpx (sync)
resp = httpx.get(url, follow_redirects=True)
resp.raise_for_status()
text = resp.text

# requests (sync only)
resp = requests.get(url, allow_redirects=True)
resp.raise_for_status()
text = resp.text
```

#### Manually adding tasks to the event loop

Recall that the results of awaiting `asyncio.gather` is always a list. Sometimes you might want more control over the data structure housing your tasks or the means of adding tasks than is offered by `asyncio.gather`. If so you can manually add tasks to the event loop like so:

```python
# Using asyncio.gather
async def download_pokemon_list() -> list[tuple[int, str]]:
    """Download a list of pokemon from 'pokemondb' using  `asyncio.gather`."""
    coroutines = [download_single_pokemon(num) for num in range(1, 21)]
    tasks = asyncio.gather(*coroutines)
    results = await tasks
    return results


# Manual method
async def download_pokemon_list() -> list[tuple[int, str]]:
    """Download a list of pokemon from 'pokemondb'.

    Manually get the event loop, create and await tasks."""
    coroutines = [download_single_pokemon(num) for num in range(1, 21)]
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(c) for c in coroutines]
    results = [await t for t in tasks]
    return results
```

As of Python 3.11 you can add tasks to task groups like so:

```python
# Manually add tasks to task group
async def download_pokemon_list() -> list[tuple[int, str]]:
    """Download a list of pokemon from 'pokemondb' using  a task group."""
    async with asyncio.TaskGroup() as tg:
        results = [tg.create_task(download_single_pokemon(num)) for num in range(1, 21)]
    return [result.result() for result in results]
```

Here are some advantages of using an `asyncio.TaskGroup`:

- The tasks automatically start when the `asyncio.TaskGroup` context block ends
- All running tasks are cancelled automatically if one task raises an exception
- All running tasks are cancelled if the task group itself is cancelled

#### Alternative method for starting async from sync

So far we've only started an event loop and run a single async **coroutine function** from our sync code using `asyncio.run`. Here's an alternative approach where we create and gather tasks to run from a normal (non-async) function, and then we create an event loop and run the tasks until they are complete:

```python
def coordinate_from_sync():
    """Start `download_single_pokemon` tasks and run from a sync function."""
    coroutines = [download_single_pokemon(num) for num in range(1, 21)]
    tasks = asyncio.gather(*coroutines)
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(tasks)
```

### Threading example

While `async`/`await` is my preferred approach for running **concurrent I/O-bound** work, it has limitations.

1. Writing the code looks different. You need to architect your code to use the new `async`/`await` syntax.
2. You need to use `async`-capable libraries to run code concurrently. Recall, we couldn't use `requests` for making `async` requests and had to use `aiohttp` instead. Sometimes there is no such library to do what you want to do (although, usually there is).

If you can't (or don't want to) use `async`/`await` to run your **I/O-bound** work concurrently, you can use threads instead. Here's what it looks like converting our synchronous Pokémon example to run concurrently with threads:

```python
# web/3_threaded.py
"""Download the first 20 pokemon with threads."""
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable

import requests
from bs4 import BeautifulSoup
from rich import print


def main() -> None:
    print("Starting tasks...", flush=True)
    t0 = time.time()
    results = download_pokemon_list()
    total_seconds = time.time() - t0
    print(
        f"\n[bold green]Code run in [cyan]{total_seconds:,.2f}[green] seconds.",
        flush=True,
    )
    print(f"\n{results=}", flush=True)


TaskType = tuple[Callable[..., Any], tuple[Any, ...], dict[str, Any]]


def download_pokemon_list() -> list[tuple[int, str]]:
    """Download a list of pokemon from 'pokemondb'."""
    print("Defining tasks...", flush=True)
    tasks: list[TaskType] = [
        # Function, args, kwargs
        (download_single_pokemon, (num,), {})
        for num in range(1, 21)
    ]
    print("Kick off threaded tasks...", flush=True)
    with ThreadPoolExecutor() as executor:
        work = [executor.submit(func, *args, **kwargs) for func, args, kwargs in tasks]
        print("Waiting for downloads...", flush=True)
    print("Done", flush=True)
    return [future.result() for future in work]


def download_single_pokemon(pokemon_num: int = 1) -> tuple[int, str]:
    """Get a pokemon from 'pokemondb' by its pokedex number."""
    print(
        f"[yellow]Downloading pokemon {pokemon_num:02}... [/yellow]",
        flush=True,
    )
    url = f"https://pokemondb.net/pokedex/{pokemon_num}"
    resp = requests.get(url, allow_redirects=True)
    resp.raise_for_status()
    header = get_h1(resp.text)
    print(
        f"[green]Retrieved [magenta]{pokemon_num:02}={header}",
        flush=True,
    )
    return (pokemon_num, header)


def get_h1(html: str) -> str:
    """Parse the HTML and return the first H1 tag."""
    soup = BeautifulSoup(html, "html.parser")
    return soup.h1.text


if __name__ == "__main__":
    main()
```

Here's terminal output from running that code:

```bash
❯ python web/3_threaded.py
Starting coordinating function...
Defining tasks...
Kick off threaded tasks...
Downloading pokemon 01...
Downloading pokemon 02...
Downloading pokemon 03...
Downloading pokemon 04...
Downloading pokemon 05...
Downloading pokemon 06...
Downloading pokemon 07...
Downloading pokemon 08...
Waiting for downloads...
Retrieved 01=Bulbasaur
Downloading pokemon 09...
Retrieved 07=Squirtle
Downloading pokemon 10...
Retrieved 02=Ivysaur
Downloading pokemon 11...
Retrieved 06=Charizard
Downloading pokemon 12...
Retrieved 05=Charmeleon
Retrieved 03=Venusaur
Downloading pokemon 13...
Downloading pokemon 14...
Retrieved 04=Charmander
Retrieved 08=Wartortle
Downloading pokemon 15...
Downloading pokemon 16...
Retrieved 10=Caterpie
Downloading pokemon 17...
Retrieved 09=Blastoise
Downloading pokemon 18...
Retrieved 11=Metapod
Downloading pokemon 19...
Retrieved 14=Kakuna
Downloading pokemon 20...
Retrieved 12=Butterfree
Retrieved 15=Beedrill
Retrieved 16=Pidgey
Retrieved 13=Weedle
Retrieved 17=Pidgeotto
Retrieved 18=Pidgeot
Retrieved 19=Rattata
Retrieved 20=Raticate
Done

Code run in 1.77 seconds.

results=[(1, 'Bulbasaur'), (2, 'Ivysaur'), (3, 'Venusaur'), (4, 'Charmander'),
(5, 'Charmeleon'), (6, 'Charizard'), (7, 'Squirtle'), (8, 'Wartortle'), (9,
'Blastoise'), (10, 'Caterpie'), (11, 'Metapod'), (12, 'Butterfree'), (13,
'Weedle'), (14, 'Kakuna'), (15, 'Beedrill'), (16, 'Pidgey'), (17, 'Pidgeotto'),
(18, 'Pidgeot'), (19, 'Rattata'), (20, 'Raticate')]
```

And here's a video showing the code executing in real time with color:

07_WEB_THREADED_VIDEO

Notice how the executed print statement order is a little more chaotic than either the synchronous script or the async script. Some requests are kicked off immediately, and other requests don't kick off until some other threads have received response data. And as with `async`/`await` code, the resulsts come back out of order compared to the requests. The net result, however, is that the speed of threaded code is comprable to `async`/`await` code (<2 seconds).

What changes did we make to run code with threads? The difference primarily lies in `doanload_pokemon_list`:

```python
# Sync
def download_pokemon_list() -> list[tuple[int, str]]:
    """Download a list of pokemon from 'pokemondb'."""
    return [download_single_pokemon(num) for num in range(1, 21)]

# Threads
from concurrent.futures import ThreadPoolExecutor
...

def download_pokemon_list() -> list[tuple[int, str]]:
    """Download a list of pokemon from 'pokemondb'."""
    print("Defining tasks...", flush=True)
    tasks: list[TaskType] = [
        # Function, args, kwargs
        (download_single_pokemon, (num,), {})
        for num in range(1, 21)
    ]
    print("Kick off threaded tasks...", flush=True)
    with ThreadPoolExecutor() as executor:
        work = [executor.submit(func, *args, **kwargs) for func, args, kwargs in tasks]
        print("Waiting for downloads...", flush=True)
    print("Done", flush=True)
    return [future.result() for future in work]
```

There a few ways to run threads in Python, but I think the `ThreadPoolExecutor` is the nicest API, so we used that. First we open a `with` block context manager for the `ThreadPoolExecutor` to handle creating, running, and cleaning up thread tasks. Then, instead of calling our `download_single_pokemon` function directly, as we do when running code synchrously or with async **coroutines**, we call `executor.submit`, passing in the function (uncalled), `args` and `kwargs`.

The return value of `exector.submit` is a thread `Future` which holds the future return value of its associated thread task function. After the context manager closes, we are garaunteed that all thread task functions have finished and all threads have closed. Then we can call `.result()` on each thread `Future` to get the result of each thread task function.

## Concurrency safety and locks

As our code runs, it frequently enters "invalid states". An "invalid state" means that the data you are working with is "wrong" (either by itself or in the context of other data) for some reason or another. Usually the code is invalid briefly and is fixed later in the code. When our code runs synchronously, we can usually garauntee that by the time the code finishes running, all "invalid states" are corrected, and the end result is that all data is "valid".

Example of one bank transferring $20 to another bank:

```python
bank_data = {
  "bank_1": 100, # dollars
  "bank_2": 100, # dollars
}
total = bank_data["bank_1"] + bank_data["bank_2"] # 200

# In "valid state"
assert bank_data["bank_1"] + bank_data["bank_2"] == total # 200


bank_data["bank_1"] - 20

# In "invalid state"
assert bank_data["bank_1"] + bank_data["bank_2"] != total # 180

bank_data["bank_2"] + 20

# Back to "valid state"
assert bank_data["bank_1"] + bank_data["bank_2"] == total # 200
```

However, when code runs concurrently, it is possible for one task to bring your data to a temporary "invalid state" and then switch tasks and have another task use the data from the "invalid state" resulting in confusing bugs. Such bugs are often said to be the result of a "race condition", where two tasks "race" towards a goal and bungle each others shared resources in the process. One of our best tools for preventing "race condition" bugs is through **locks** that lock code execution to one task while the lock is in place. More on **locks** soon.

Race condition bugs can occur in both `async`/`await` code running on a single thread and **threaded** code because both can create "invalid states" and release code execution so that another task sees the "invalid state" shared resource. However, threaded code is more likely to result in a bug than `async`/`await` code mainly because of who controls when one task gives up execution to another task.

With `async`/`await` code, we explicitly set places in our code to wait and let another task start working (with the `await` statement or through `async with` context managers). Between those special waiting places, we are sure the same task is executing code continuously.

However, with **threaded** code, the **CPU** controls which task is running at any given moment, and the **CPU** tends to rapidly alternate between different tasks, even changing from one task (one thread) to another mid-line of code. Therefore, there are more places that one task could create "invalid state" for another task to see. Ensuring tasks can safely run with threads in such a way that tasks never switch during an invalid state is called "thread-safety".

### Sync bank transfers

Let's look at some examples. First we'll expand our banking example above. The example makes banking transactions between bank customers synchronously, one after the other:

```python
# locks/1_sync.py
"""Run simulated banking transactions."""
import random
import time

from rich import print

BANK_DATA = {
    "bank_1": 1000,
    "bank_2": 1000,
    "bank_3": 1000,
    "bank_4": 1000,
    "bank_5": 1000,
}


def main() -> None:
    """Run the main program."""
    t0 = time.time()
    print(f"\ninitial={BANK_DATA}\n", flush=True)
    run_transactions()
    total_seconds = time.time() - t0

    print(f"\n\nfinal={BANK_DATA}", flush=True)
    print(f"sum={sum(BANK_DATA.values())}", flush=True)
    print(
        f"\n[bold green]Code run in [cyan]{total_seconds:,.2f}[green] seconds.",
        flush=True,
    )


def run_transactions() -> None:
    """Run a series of bank transactions."""
    for _ in range(20):
        banks = list(BANK_DATA.keys())
        sending_bank = random.choice(banks)
        banks.remove(sending_bank)
        receiving_bank = random.choice(list(banks))
        amount = random.randint(1, 100)
        run_transaction(sending_bank, receiving_bank, amount)


def run_transaction(sending_bank: str, receiving_bank: str, amount) -> None:
    """Run a bank transaction."""
    verify_user()
    update_bank(sending_bank, -amount)
    update_bank(receiving_bank, amount)
    print(".", end="", flush=True)


def verify_user() -> None:
    """Simulate verifying the user can make the transaction."""
    time.sleep(0.1)


def update_bank(bank_name: str, amount: int) -> None:
    """Update the bank data."""
    amount_before = BANK_DATA[bank_name]
    time.sleep(0.0001)
    new_amount = amount_before + amount
    BANK_DATA[bank_name] = new_amount
    time.sleep(0.0001)


if __name__ == "__main__":
    main()
```

Here's the results of that python script run on the command line:

```bash
❯ python locks/1_sync.py

initial={'bank_1': 1000, 'bank_2': 1000, 'bank_3': 1000, 'bank_4': 1000,
'bank_5': 1000}

....................

final={'bank_1': 846, 'bank_2': 986, 'bank_3': 1072, 'bank_4': 1056, 'bank_5':
1040}
sum=5000

Code run in 2.08 seconds.
```

And a video in real time, with color:

08_LOCKS_SYNC_VIDEO

The example is obviously contrived. It uses the `random` module to randomly make twentry bank account balance transfers between five possible banks. It uses `time.sleep` to simulate talking to external **I/O** services. Conveniently for us, our operating system treats `time.sleep` as an **I/O-bound** operation. One thread can make progress on its `sleep` while another thread actively executes code.

Also, notice there are a couple opportunities for "invalid state" in this example.

1. Like our previous example, in `run_transaction` the state is invalid between subtracting money from one bank account and adding it to the next.
2. In `update_bank` first we get a bank's account balance and, after a tiny delay, we update the bank account balance. In between the retrieving and the updating, the bank account balance information is stale, and another bank account could theoretically alter the balance in that window--an opportunity for "invalid state".

However, since the code runs synchronously, we can garauntee that these "invalid states" are fixed before a transaction finishes, and thus all is correct when the script completes.

### Unsafe async bank transfers

Let's speed up these bank transfers by converting them to the `async`/`await` syntax to run all bank transfers concurrently.

```python
# locks/2_async_unsafe.py
"""Run simulated banking transactions."""
import asyncio
import random
import time

from rich import print

BANK_DATA = {
    "bank_1": 1000,
    "bank_2": 1000,
    "bank_3": 1000,
    "bank_4": 1000,
    "bank_5": 1000,
}


def main() -> None:
    """Run the main program."""
    t0 = time.time()
    print(f"\ninitial={BANK_DATA}\n", flush=True)
    asyncio.run(run_transactions())
    total_seconds = time.time() - t0

    print(f"\n\nfinal={BANK_DATA}", flush=True)
    print(f"sum={sum(BANK_DATA.values())}", flush=True)
    print(
        f"\n[bold green]Code run in [cyan]{total_seconds:,.2f}[green] seconds.",
        flush=True,
    )


async def run_transactions() -> None:
    """Run a series of bank transactions."""
    coroutines = []
    for _ in range(20):
        banks = list(BANK_DATA.keys())
        sending_bank = random.choice(banks)
        banks.remove(sending_bank)
        receiving_bank = random.choice(list(banks))
        amount = random.randint(1, 100)
        coroutines.append(run_transaction(sending_bank, receiving_bank, amount))
    await asyncio.gather(*coroutines)


async def run_transaction(sending_bank: str, receiving_bank: str, amount) -> None:
    """Run a bank transaction."""
    await verify_user()
    await update_bank(sending_bank, -amount)
    await update_bank(receiving_bank, amount)
    print(".", end="", flush=True)


async def verify_user() -> None:
    """Simulate verifying the user can make the transaction."""
    await asyncio.sleep(0.1)


async def update_bank(bank_name: str, amount: int) -> None:
    """Update the bank data."""
    amount_before = BANK_DATA[bank_name]
    await asyncio.sleep(0.0001)
    new_amount = amount_before + amount
    BANK_DATA[bank_name] = new_amount
    await asyncio.sleep(0.0001)


if __name__ == "__main__":
    main()
```

Here's the results of that python script run on the command line:

```bash
❯ python locks/2_async_unsafe.py

initial={'bank_1': 1000, 'bank_2': 1000, 'bank_3': 1000, 'bank_4': 1000,
'bank_5': 1000}

....................

final={'bank_1': 1002, 'bank_2': 966, 'bank_3': 939, 'bank_4': 1073, 'bank_5':
1059}
sum=5039

Code run in 0.15 seconds.
```

And a video in real time, with color:

09_LOCKS_ASYNC_UNSAFE

Since I already explained the `async`/`await` changes in detail for web scraping above, I won't go into detail on the changes in this script. Suffice it to say, we convert a bunch of functions from `def function` to `async def function` and add `await` statements to wait on **coroutine functions** and **I/O-bound** work. One notible change is I converted all `time.sleep` functions to `asyncio.sleep` functions which are the same but awaitable with the `await` keyword.

What are the results of changing this function to `async`/`await` concurrent tasks? For one it completed more than 10X faster. For antoher, _it created a race condition bug_. The bug arises because of the two invalid state opportunities I listed previously:

1. In `run_transaction` the state is invalid between subtracting money from one bank account and adding it to the next. One bank fund transfer can use the "invalid" funds from one bank account that is mid-transfer of another transaction.
2. In `update_bank` first we get a bank's account balance and, after a tiny delay, we update the bank account balance. In between the retrieving and the updating, the bank account balance information is stale, and another bank account could theoretically alter the balance in that window--an opportunity for "invalid state".

### Safe async bank transfers

How do we fix this bug? The simplest fix is to introduce a **lock** which looks like this:

```python
# locks/2_async_safe.py
"""Run simulated banking transactions."""
import asyncio
import random
import time

from rich import print

BANK_DATA = {
    "bank_1": 1000,
    "bank_2": 1000,
    "bank_3": 1000,
    "bank_4": 1000,
    "bank_5": 1000,
}

TRANSACTION_LOCK = asyncio.Lock()


def main() -> None:
    """Run the main program."""
    t0 = time.time()
    print(f"\ninitial={BANK_DATA}\n", flush=True)
    asyncio.run(run_transactions())
    total_seconds = time.time() - t0

    print(f"\n\nfinal={BANK_DATA}", flush=True)
    print(f"sum={sum(BANK_DATA.values())}", flush=True)
    print(
        f"\n[bold green]Code run in [cyan]{total_seconds:,.2f}[green] seconds.",
        flush=True,
    )


async def run_transactions() -> None:
    """Run a series of bank transactions."""
    coroutines = []
    for _ in range(20):
        banks = list(BANK_DATA.keys())
        sending_bank = random.choice(banks)
        banks.remove(sending_bank)
        receiving_bank = random.choice(list(banks))
        amount = random.randint(1, 100)
        coroutines.append(run_transaction(sending_bank, receiving_bank, amount))
    await asyncio.gather(*coroutines)


async def run_transaction(sending_bank: str, receiving_bank: str, amount) -> None:
    """Run a bank transaction."""
    await verify_user()
    async with TRANSACTION_LOCK:
        await update_bank(sending_bank, -amount)
        await update_bank(receiving_bank, amount)
    print(".", end="", flush=True)


async def verify_user() -> None:
    """Simulate verifying the user can make the transaction."""
    await asyncio.sleep(0.1)


async def update_bank(bank_name: str, amount: int) -> None:
    """Update the bank data."""
    amount_before = BANK_DATA[bank_name]
    await asyncio.sleep(0.0001)
    new_amount = amount_before + amount
    BANK_DATA[bank_name] = new_amount
    await asyncio.sleep(0.0001)


if __name__ == "__main__":
    main()
```

Here's the results of that python script run on the command line:

```bash
❯ python locks/2_async_safe.py                                     ✭ ✱ 14:30:43

initial={'bank_1': 1000, 'bank_2': 1000, 'bank_3': 1000, 'bank_4': 1000,
'bank_5': 1000}

....................

final={'bank_1': 966, 'bank_2': 1122, 'bank_3': 1034, 'bank_4': 931, 'bank_5':
947}
sum=5000

Code run in 0.24 seconds.
```

And a video in real time, with color:

10_LOCKS_ASYNC_SAFE_VIDEO

The only changes between this script and the previous script are here:

```python
import asyncio
...

TRANSACTION_LOCK = asyncio.Lock()
...

async def run_transaction(sending_bank: str, receiving_bank: str, amount) -> None:
    ...
    async with TRANSACTION_LOCK:
        await update_bank(sending_bank, -amount)
        await update_bank(receiving_bank, amount)
```

We use a `asyncio.Lock()` while executing the two `update_bank` functions. The lock prevents the **event loop** from releasing the current task to other tasks when it hits `await` statements for I/O-bound tasks as it normally does. The result? The bug goes away. Because of the lock, the task fixes the "invalid state" **_before_** releasing execution to another task. However, the script also runs slower because it doesn't release for some of the waiting steps and thus runs less code concurrently.

### Unsafe threaded bank transfers

Alternatively to `async`/`await`, we can perform the bank transfers concurrently with **threads**. Here's how that looks:

```python
# locks/3_threaded_unsafe.py
"""Run simulated banking transactions."""
import random
import time
from concurrent.futures import ThreadPoolExecutor

from rich import print

BANK_DATA = {
    "bank_1": 1000,
    "bank_2": 1000,
    "bank_3": 1000,
    "bank_4": 1000,
    "bank_5": 1000,
}


def main() -> None:
    """Run the main program."""
    t0 = time.time()
    print(f"\ninitial={BANK_DATA}\n", flush=True)
    run_transactions()
    total_seconds = time.time() - t0

    print(f"\n\nfinal={BANK_DATA}", flush=True)
    print(f"sum={sum(BANK_DATA.values())}", flush=True)
    print(
        f"\n[bold green]Code run in [cyan]{total_seconds:,.2f}[green] seconds.",
        flush=True,
    )


def run_transactions() -> None:
    """Run a series of bank transactions."""
    tasks = []
    for _ in range(20):
        banks = list(BANK_DATA.keys())
        sending_bank = random.choice(banks)
        banks.remove(sending_bank)
        receiving_bank = random.choice(list(banks))
        amount = random.randint(1, 100)
        tasks.append(
            # func, args, kwargs
            (run_transaction, (sending_bank, receiving_bank), {"amount": amount})
        )
    with ThreadPoolExecutor() as executor:
        [executor.submit(func, *args, **kwargs) for func, args, kwargs in tasks]


def run_transaction(sending_bank: str, receiving_bank: str, amount) -> None:
    """Run a bank transaction."""
    verify_user()
    update_bank(sending_bank, -amount)
    update_bank(receiving_bank, amount)
    print(".", end="", flush=True)


def verify_user() -> None:
    """Simulate verifying the user can make the transaction."""
    time.sleep(0.1)


def update_bank(bank_name: str, amount: int) -> None:
    """Update the bank data."""
    amount_before = BANK_DATA[bank_name]
    time.sleep(0.0001)
    new_amount = amount_before + amount
    BANK_DATA[bank_name] = new_amount
    time.sleep(0.0001)


if __name__ == "__main__":
    main()
```

Here's the results of that python script run on the command line:

```bash
❯ python locks/3_threaded_unsafe.py                                ✭ ✱ 14:48:28

initial={'bank_1': 1000, 'bank_2': 1000, 'bank_3': 1000, 'bank_4': 1000,
'bank_5': 1000}

....................

final={'bank_1': 880, 'bank_2': 903, 'bank_3': 1034, 'bank_4': 1066, 'bank_5':
1135}
sum=5018

Code run in 0.36 seconds.
```

And a video in real time, with color:

11_LOCKS_THREAEDED_UNSAFE_VIDEO

The difference between this code and the synchronous code is that the bank transaction tasks are run in a `ThreadPoolExecutor` in the `run_transactions` function:

```python
from concurrent.futures import ThreadPoolExecutor
...

def run_transactions() -> None:
    tasks = []
    for _ in range(20):
        ...
        tasks.append(
            # func, args, kwargs
            (run_transaction, (sending_bank, receiving_bank), {"amount": amount})
        )
    with ThreadPoolExecutor() as executor:
        [executor.submit(func, *args, **kwargs) for func, args, kwargs in tasks]
```

Here we see the same race condition bug as we do with the `async`/`await` script before adding locks. And the fix is almost identical to the `async`/`await` fix: using a lock.

### Safe threaded bank transfers

Here's the code for safe threaded bank transfers:

```python
# locks/3_threaded_safe.py
"""Run simulated banking transactions."""
import random
import time
from concurrent.futures import ThreadPoolExecutor
import threading

from rich import print

BANK_DATA = {
    "bank_1": 1000,
    "bank_2": 1000,
    "bank_3": 1000,
    "bank_4": 1000,
    "bank_5": 1000,
}

TRANSACTION_LOCK = threading.RLock()


def main() -> None:
    """Run the main program."""
    t0 = time.time()
    print(f"\ninitial={BANK_DATA}\n", flush=True)
    run_transactions()
    total_seconds = time.time() - t0

    print(f"\n\nfinal={BANK_DATA}", flush=True)
    print(f"sum={sum(BANK_DATA.values())}", flush=True)
    print(
        f"\n[bold green]Code run in [cyan]{total_seconds:,.2f}[green] seconds.",
        flush=True,
    )


def run_transactions() -> None:
    """Run a series of bank transactions."""
    tasks = []
    for _ in range(20):
        banks = list(BANK_DATA.keys())
        sending_bank = random.choice(banks)
        banks.remove(sending_bank)
        receiving_bank = random.choice(list(banks))
        amount = random.randint(1, 100)
        tasks.append(
            # func, args, kwargs
            (run_transaction, (sending_bank, receiving_bank), {"amount": amount})
        )
    with ThreadPoolExecutor() as executor:
        [executor.submit(func, *args, **kwargs) for func, args, kwargs in tasks]


def run_transaction(sending_bank: str, receiving_bank: str, amount) -> None:
    """Run a bank transaction."""
    verify_user()
    with TRANSACTION_LOCK:
        update_bank(sending_bank, -amount)
        update_bank(receiving_bank, amount)
    print(".", end="", flush=True)


def verify_user() -> None:
    """Simulate verifying the user can make the transaction."""
    time.sleep(0.1)


def update_bank(bank_name: str, amount: int) -> None:
    """Update the bank data."""
    amount_before = BANK_DATA[bank_name]
    time.sleep(0.0001)
    new_amount = amount_before + amount
    BANK_DATA[bank_name] = new_amount
    time.sleep(0.0001)


if __name__ == "__main__":
    main()
```

Here's the results of that python script run on the command line:

```bash
❯ python locks/3_threaded_safe.py

initial={'bank_1': 1000, 'bank_2': 1000, 'bank_3': 1000, 'bank_4': 1000,
'bank_5': 1000}

....................

final={'bank_1': 1071, 'bank_2': 894, 'bank_3': 1029, 'bank_4': 1129, 'bank_5':
877}
sum=5000

Code run in 0.35 seconds.
```

And a video in real time, with color:

12_LOCKS_THREAEDED_SAFE_VIDEO

Here's just the code changed to add the locks. **Notice** we use `threading.RLock()` instead of `threading.Lock()`. `threading.RLock()` is usually what you want as it wont deadlock when it encounters the same lock (for instance with recursive code).

```python
import threading
...

TRANSACTION_LOCK = threading.RLock()
...

def run_transaction(sending_bank: str, receiving_bank: str, amount) -> None:
    ...
    with TRANSACTION_LOCK:
        update_bank(sending_bank, -amount)
        update_bank(receiving_bank, amount)
```

As with `async`/`await`, a thread lock fixes the "race condition" bug and slightly slows down the code.

## CPU bound parallelism

As stated earlier in this post, normally Python only executes one instruction at a time, even with **threads** due to the **GIL**. All of our examples thus far have achieved **concurrency** by allowing Python code to run in the foreground while **I/O** waiting happens in the background. Is it possible to execute multiple Python processes in **parallel**, leveraging all our **CPU cores** instead of just one? Yes, with the `multiprocessing` module.

### CPU-bound Sync example

I'll lay out a contrived example to show how multiprocessing works. First, lets see an example of **CPU-bound** bound (no **I/O** work) code run synchrounously:

```python
# cpu_bound/1_sync.py
"""Do some CPU bound work synchronously."""
import time

from rich import print


def main():
    print("Starting tasks...", flush=True)
    t0 = time.time()
    results = do_lots_of_math()
    total_seconds = time.time() - t0
    print(
        f"\n[bold green]Code run in [cyan]{total_seconds:,.2f}[green] seconds.",
        flush=True,
    )
    print(f"\n{results=}", flush=True)


def do_lots_of_math() -> list[float]:
    return [do_math_once(num) for num in range(1, 21)]


def do_math_once(starting_number: int = 1) -> float:
    """Do some CPU bound work."""
    print(f"[yellow]Doing math, {starting_number=}...", flush=True)
    x = starting_number
    for _ in range(2_000_000):
        x **= 4
        x **= 0.25
        x **= 2
        x **= 0.5
        x += 1
    print(f"[green]Done with math, {starting_number=}.", flush=True)
    return x


if __name__ == "__main__":
    main()
```

Here's the results of that python script run on the command line:

```bash
❯ python cpu_bound/1_sync.py
Starting tasks...
Doing math, starting_number=1...
Done with math, starting_number=1.
Doing math, starting_number=2...
Done with math, starting_number=2.
Doing math, starting_number=3...
Done with math, starting_number=3.
Doing math, starting_number=4...
Done with math, starting_number=4.
Doing math, starting_number=5...
Done with math, starting_number=5.
Doing math, starting_number=6...
Done with math, starting_number=6.
Doing math, starting_number=7...
Done with math, starting_number=7.
Doing math, starting_number=8...
Done with math, starting_number=8.
Doing math, starting_number=9...
Done with math, starting_number=9.
Doing math, starting_number=10...
Done with math, starting_number=10.
Doing math, starting_number=11...
Done with math, starting_number=11.
Doing math, starting_number=12...
Done with math, starting_number=12.
Doing math, starting_number=13...
Done with math, starting_number=13.
Doing math, starting_number=14...
Done with math, starting_number=14.
Doing math, starting_number=15...
Done with math, starting_number=15.
Doing math, starting_number=16...
Done with math, starting_number=16.
Doing math, starting_number=17...
Done with math, starting_number=17.
Doing math, starting_number=18...
Done with math, starting_number=18.
Doing math, starting_number=19...
Done with math, starting_number=19.
Doing math, starting_number=20...
Done with math, starting_number=20.

Code run in 10.57 seconds.

results=[2000001.0, 2000002.0, 2000003.0, 2000004.0, 2000005.0, 2000006.0,
2000007.0, 2000008.0, 2000009.0, 2000010.0, 2000011.0, 2000012.0, 2000013.0,
2000014.0, 2000015.0, 2000016.0, 2000017.0, 2000018.0, 2000019.0, 2000020.0]
```

And a video of the code run in real time, with color, alongside my task manager:

13_CPU_BOUND_SYNC

Notice that the operations run sequentially, and take a little over 10 seconds. Also notice that one of my CPU cores shoot up to 100% usage during that time and the others stay lower.

The code performs simple, non-sensical math operations run over a loop with many iterations. The math isn't important, just the fact that it takes some time and there are no **I/O** processes.

### CPU-bound threaded example

I know I said threading won't speed up CPU-bound operations, but let's try anyways just to see what happens:

```python
# cpu_bound/2_threaded_no_improvement.py
"""Do some CPU bound work synchronously."""
import time
from concurrent.futures import ThreadPoolExecutor as PoolExecutor
from typing import Any, Callable

from rich import print


def main():
    print("Starting tasks...", flush=True)
    t0 = time.time()
    results = do_lots_of_math()
    total_seconds = time.time() - t0
    print(
        f"\n[bold green]Code run in [cyan]{total_seconds:,.2f}[green] seconds.",
        flush=True,
    )
    print(f"\n{results=}", flush=True)


TaskType = tuple[Callable[..., Any], tuple[Any, ...], dict[str, Any]]


def do_lots_of_math() -> list[float]:
    print("Defining tasks...", flush=True)
    tasks: list[TaskType] = [
        # Function, args, kwargs
        (do_math_once, (num,), {})
        for num in range(1, 21)
    ]
    print("Kick off multiprocess tasks...", flush=True)
    with PoolExecutor() as executor:
        work = [executor.submit(func, *args, **kwargs) for func, args, kwargs in tasks]
        print("Waiting for work...", flush=True)
    print("Done with work", flush=True)
    return [future.result() for future in work]


def do_math_once(starting_number: int = 1) -> float:
    """Do some CPU bound work."""
    print(f"[yellow]Doing math, {starting_number=}...", flush=True)
    x = starting_number
    for _ in range(2_000_000):
        x **= 4
        x **= 0.25
        x **= 2
        x **= 0.5
        x += 1
    print(f"[green]Done with math, {starting_number=}.", flush=True)
    return x


if __name__ == "__main__":
    main()
```

Here's the results of that python script run on the command line:

```bash
❯ python cpu_bound/2_threaded_no_improvement.py
Starting tasks...
Defining tasks...
Kick off multiprocess tasks...
Doing math, starting_number=1...
Doing math, starting_number=2...
Doing math, starting_number=3...
Doing math, starting_number=4...
Doing math, starting_number=5...
Doing math, starting_number=6...
Doing math, starting_number=7...
Doing math, starting_number=8...
Waiting for work...
Done with math, starting_number=7.
Doing math, starting_number=9...
Done with math, starting_number=3.
Doing math, starting_number=10...
Done with math, starting_number=4.
Doing math, starting_number=11...
Done with math, starting_number=1.
Doing math, starting_number=12...
Done with math, starting_number=5.
Doing math, starting_number=13...
Done with math, starting_number=6.
Doing math, starting_number=14...
Done with math, starting_number=2.
Doing math, starting_number=15...
Done with math, starting_number=8.
Doing math, starting_number=16...
Done with math, starting_number=9.
Doing math, starting_number=17...
Done with math, starting_number=13.
Doing math, starting_number=18...
Done with math, starting_number=10.
Done with math, starting_number=11.
Doing math, starting_number=19...
Doing math, starting_number=20...
Done with math, starting_number=16.
Done with math, starting_number=14.
Done with math, starting_number=15.
Done with math, starting_number=12.
Done with math, starting_number=17.
Done with math, starting_number=18.
Done with math, starting_number=19.
Done with math, starting_number=20.
Done with work

Code run in 10.79 seconds.

results=[2000001.0, 2000002.0, 2000003.0, 2000004.0, 2000005.0, 2000006.0,
2000007.0, 2000008.0, 2000009.0, 2000010.0, 2000011.0, 2000012.0, 2000013.0,
2000014.0, 2000015.0, 2000016.0, 2000017.0, 2000018.0, 2000019.0, 2000020.0]
```

And a video of the code run in real time, with color, alongside my task manager:

14_CPU_BOUND_THREADED

It looks like the threads are running at the same time since the print statements for the operations occur out of order. However the run time is about the same as the synchronous operations script.

### CPU-bound multiprocessing example

In this final example we use the multiprocessing module to run the **CPU-bound** operations in parallel on multiple cores.

```python
# cpu_bound/3_multiprocess.py
"""Do some CPU bound work synchronously."""
import time
from concurrent.futures.process import ProcessPoolExecutor as PoolExecutor
from typing import Any, Callable

from rich import print


def main():
    print("Starting tasks...", flush=True)
    t0 = time.time()
    results = do_lots_of_math()
    total_seconds = time.time() - t0
    print(
        f"\n[bold green]Code run in [cyan]{total_seconds:,.2f}[green] seconds.",
        flush=True,
    )
    print(f"\n{results=}", flush=True)


TaskType = tuple[Callable[..., Any], tuple[Any, ...], dict[str, Any]]


def do_lots_of_math() -> list[float]:
    print("Defining tasks...", flush=True)
    tasks: list[TaskType] = [
        # Function, args, kwargs
        (do_math_once, (num,), {})
        for num in range(1, 21)
    ]
    print("Kick off multiprocess tasks...", flush=True)
    with PoolExecutor() as executor:
        work = [executor.submit(func, *args, **kwargs) for func, args, kwargs in tasks]
        print("Waiting for work...", flush=True)
    print("Done with work", flush=True)
    return [future.result() for future in work]


def do_math_once(starting_number: int = 1) -> float:
    """Do some CPU bound work."""
    print(f"[yellow]Doing math, {starting_number=}...", flush=True)
    x = starting_number
    for _ in range(2_000_000):
        x **= 4
        x **= 0.25
        x **= 2
        x **= 0.5
        x += 1
    print(f"[green]Done with math, {starting_number=}.", flush=True)
    return x


if __name__ == "__main__":
    main()
```

Here's the results of that python script run on the command line:

```bash
❯ python cpu_bound/3_multiprocess.py                             ✗ ✭ ✱ 16:19:17
Starting tasks...
Defining tasks...
Kick off multiprocess tasks...
Waiting for work...
Doing math, starting_number=1...
Doing math, starting_number=2...
Doing math, starting_number=3...
Doing math, starting_number=4...
Done with math, starting_number=4.
Doing math, starting_number=5...
Done with math, starting_number=3.
Doing math, starting_number=6...
Done with math, starting_number=1.
Doing math, starting_number=7...
Done with math, starting_number=2.
Doing math, starting_number=8...
Done with math, starting_number=5.
Doing math, starting_number=9...
Done with math, starting_number=6.
Doing math, starting_number=10...
Done with math, starting_number=7.
Doing math, starting_number=11...
Done with math, starting_number=8.
Doing math, starting_number=12...
Done with math, starting_number=9.
Doing math, starting_number=13...
Done with math, starting_number=10.
Doing math, starting_number=14...
Done with math, starting_number=11.
Doing math, starting_number=15...
Done with math, starting_number=12.
Doing math, starting_number=16...
Done with math, starting_number=13.
Doing math, starting_number=17...
Done with math, starting_number=14.
Doing math, starting_number=18...
Done with math, starting_number=15.
Doing math, starting_number=19...
Done with math, starting_number=16.
Doing math, starting_number=20...
Done with math, starting_number=17.
Done with math, starting_number=18.
Done with math, starting_number=19.
Done with math, starting_number=20.
Done with work

Code run in 2.99 seconds.

results=[2000001.0, 2000002.0, 2000003.0, 2000004.0, 2000005.0, 2000006.0,
2000007.0, 2000008.0, 2000009.0, 2000010.0, 2000011.0, 2000012.0, 2000013.0,
2000014.0, 2000015.0, 2000016.0, 2000017.0, 2000018.0, 2000019.0, 2000020.0]
```

And a video of the code run in real time, with color, alongside my task manager:

15_CPU_BOUND_MULTIPROCESSING

This time you can can see that all four of my **CPU cores** are fully utilized and the script runs a little over 3X as fast which is in line with my expectations. We could expect maybe 4X as fast for 4 **CPU cores**, minus some speed for the tasks that aren't run in tasks and the overhead.

Also, notice the difference between running **threaded** code and **multiprocessing** code is quite minimal since the `ProcessPoolExecutor` implements the same interface as the `ThreadPoolExecutor`, and since I aliased both to `PoolExecutor`, I only had to change one line (the rest of the code is exactly the same):

```python
from concurrent.futures import ThreadPoolExecutor as PoolExecutor
from concurrent.futures.process import ProcessPoolExecutor as PoolExecutor
```

`ProcessPoolExecutor` is great because it intelligently runs the same number of multiprocesses as my computer has **CPU cores** and cleans up those processes when the `with` block context manager closes.

## Conclusions

In this article I [discussed key terms](#defining-key-terms) related to **concurrency** in python and [gave visual explanations of the three concurrent programming paradigms](#visual-examples). Then I went through concrete examples of running concurrent **I/O-bound** Python code by [web scraping pages of a Pokémon website](#http-requests). Then I discussed ["race conditions" in concurrent code and showed how to solve them with locks](#concurrency-safety-and-locks). Finally, I [gave some examples of running **CPU-bound** python code in parallel with the multiprocessing module](#cpu-bound-parallelism). I hope this intro to concurrent programing gives you ideas for speeding up your next project!