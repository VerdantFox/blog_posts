# Set, update, read, and delete cookies with Flask

tags: Python, Flask, cookies, tutorial

## Introduction

01_FLASK_COOKIES_PIC

Cookies! 🍪🍪 Tasty snack or valuable web development tool? 🤷‍♂️ For our context today, cookies are small pieces of data sent from the server to the client. The client's browser stores cookies locally and then sends the cookies back to the server with every request. Cookies are used for a variety of purposes, including session management (who's logged in?), keeping track of user settings (use dark mode?), and tracking user behavior (website analytics, ad targeting). In this short tutorial, we'll talk about how to manage cookies with the Flask web framework. We'll go over setting, updating, retrieving, and deleting cookies in Flask routes.

## Setup

We'll be using the Flask web framework. Flask is a highly customizable micro web framework written in Python. To use the framework, you'll need to [install Python](https://www.python.org/downloads/) and [set up a virtual environment](https://realpython.com/python-virtual-environments-a-primer/). Then, inside your activated Python virtual environment, run the following command line instruction to install Flask:

```bash
pip install Flask
```

Awesome, we're good to go.

## The code

[You can find a GitHub repository with the code used for this tutorial here](https://github.com/VerdantFox/flask_cookies). For this short tutorial, we'll need two files, an `app.py` file with our Flask application and a `template.html` file in the `templates/` directory for our HTML template. The project structure looks like this:

```txt
app.py
templates/
|
└── template.html
```

The `app.py` file code:

```python
from datetime import timedelta

from flask import Flask, make_response, render_template, request

app = Flask(__name__)


@app.route("/")
def read_cookies():
    """Read all the cookies."""
    return render_template("template.html", cookies=request.cookies)


@app.route("/set-cookie")
def set_cookie():
    """Set a new session cookie. The default cookie expires when the session ends."""
    response = make_response(render_template("template.html", cookies=request.cookies))
    response.set_cookie("cookie_name", "cookie_value")
    return response


@app.route("/set-path-cookie")
def set_path_cookie():
    """Set a new session cookie with the path value set.

    It will only be sent if the path matches the request path.
    It will match /set-path-cookie, /set-path-cookie/ and /set-path-cookie/anything
    """
    response = make_response(render_template("template.html", cookies=request.cookies))
    response.set_cookie(
        "path_cookie_name", "path_cookie_value", path="/set-path-cookie"
    )
    return response


@app.route("/set-expiring-cookie")
def set_expiring_cookie():
    """Set a new cookie that expires in 15 seconds."""
    response = make_response(render_template("template.html", cookies=request.cookies))
    response.set_cookie("expiring_cookie_name", "expiring_cookie_value", max_age=15)
    return response


@app.route("/set-long-lasting-cookie")
def set_long_lasting_cookie():
    """Set a new cookie that expires in 400 days (the maximum mx_cookie age)."""
    response = make_response(render_template("template.html", cookies=request.cookies))
    response.set_cookie(
        "long_cookie_name", "long_cookie_value", max_age=timedelta(days=400)
    )
    return response


@app.route("/delete-cookies")
def delete_cookies():
    """Delete all cookies we created."""
    response = make_response(render_template("template.html", cookies=request.cookies))
    response.delete_cookie("cookie_name")
    response.delete_cookie("path_cookie_name")
    response.delete_cookie("expiring_cookie_name")
    response.delete_cookie("long_cookie_name")
    return response
```

The `templates/template.html` code:

```html
<h1>Cookies:</h1>
<p>{{ cookies }}</p>
```

## Basic Flask explanation

The Flask application is built with a simple call `app = Flask(__name__)`. Flask routes are simple functions decorated with the `@app.route(ROUTE)` where `ROUTE` is the `/url/route/destination`. If a Flask application returns HTML, typically, we write the HTML in [Jinja template files](https://palletsprojects.com/p/jinja/). These are essentially HTML files that can have added Python logic, such as injected variables. Let's see how we render a Jinja template in our `read_cookies()` function.

```python
from flask import render_template, request

app = Flask(__name__)


@app.route("/")
def read_cookies():
    """Read all the cookies."""
    return render_template("template.html", cookies=request.cookies)
```

We render the template with the Flask `render_template` function, passing in our template file and any variables we want to add. We give a `cookies` parameter to `render_template`, which the Jinja template can read:

```html
<h1>Cookies:</h1>
<p>{{ cookies }}</p>
```

The `cookies` parameter passed in the `render_template` function is converted to a string in the template with `{{ cookies }}`. To run the example Flask application, we can enter the following on the command line:

```bash
flask --app app run --reload
```

The above entry generates a development Flask server that listens for requests on `localhost:5000`. If you go to `localhost:5000` in your web browser, the `read_cookies` route will call and render our `template.html` template. The first call will probably look like this since we haven't set any cookies yet. Note Flask might set some other cookies.

02_HTML_NO_COOKIES_PIC
Browser page with no cookies set.

## Reading cookies

Flask reads cookies from [the global `request` object](https://tedboy.github.io/flask/generated/generated/flask.Request.html). Recall we imported `from flask import Flask, make_response, render_template, request`. `request` is a global variable containing the current request's details. Its attributes include headers, the URL, and query string parameters. It also contains the request's **cookies**. We access those cookies with `request.cookies`.

`request.cookies` is a Python `ImmutableMultiDict` object—essentially a dictionary that can't be updated. Its immutability is a reminder that cookies are stored with the client, not the server. To update those cookies, we need to send a response to the client indicating those cookies should update. Since `request.cookies` is a special dictionary, we can extract values from it the same way we do normal dictionaries: we can call `request.cookies.get("cookie_key")` or `request.cookies["cookie_key"]` to retrieve a cookie value.

Notice that all the route functions in the above Python Flask code share the same template and read and return the currently set cookies.

## Setting cookies

To set cookies, we need to send a response to the client with cookie key-value pairs attached. The standard way to send a response in Flask is to return a rendered template (or a string). When we return a rendered template, Flask creates a response behind the scenes and sets that rendered template as the response body. Unfortunately, this leaves no way for us to attach cookies to the response. To get around this problem, we need to create the response ourselves *in* the route function to attach the cookie. Let's look at an example.

```python
from flask import make_response, render_template, request

app = Flask(__name__)


@app.route("/set-cookie")
def set_cookie():
    """Set a new session cookie. The default cookie expires when the session ends."""
    response = make_response(render_template("template.html", cookies=request.cookies))
    response.set_cookie("cookie_name", "cookie_value")
    return response
```

In the above Flask route function, we create the response object early with the `make_response` function (imported from `flask`). We supply the `make_response` function with our response body—the same `render_template` we returned in the `read_cookies()` function. `make_response` returns a [Flask.Response](https://tedboy.github.io/flask/generated/generated/flask.Response.html) object. Now that we have a `response` object to work with, we call `response.set_cookie(KEY, VAL)` to attach a cookie key-value pair to the response object. We can attach as many cookie key-value pairs as we want to the `response` object. When we `return response`, Flask sends the already built response to the client—no need to generate a new response behind the scenes in this case.

With the Flask app running, go to the URL `localhost:5000/set-cookie` in your web browser to run the above route function. You'll notice that no cookies will be listed the first time you go to this web page. What gives? Recall cookies are stored on the client's browser and sent with each request. The first time we invoke the `set_cookie()` route function, the request doesn't have any cookies set yet. The cookies are sent to the client in the response. If you call `localhost:5000/set-cookie` a second time (or `localhost:5000`), you will see the cookie key-value pair set by the first call to the `set_cookie()` route function. After the second call, the browser should look like this:

03_HTML_FIRST_COOKIE_SET_PIC
Browser page with the cookie set by /set-cookie route.

Note: if you want to *update* a cookie—change a cookie's value—call `response.set_cookie()` again, passing in the new key-value pair. If the key is the same as an existing key, the cookie will overwrite with the new value.

## Cookie expirations

By default, cookies are set as **session cookies**. **Session cookies** expire when the session ends. If you exit your browser to end your session, your browser will delete the cookies—when you open `localhost:5000` again, the cookies set by `localhost:5000/set-cookie` will be gone. If we want to make a cookie last outside of the context of the current session (or if we want them to expire before the session ends), we can instead create an **expiring cookie**. An **expiring cookie** is a cookie with an expiration set. Instead of deleting the cookie when the session ends, the browser will delete the cookie when the cookie expires.

To set a cookie expiration, use the `max_age=SECONDS` parameter, passing in the number of seconds until expiration.

```python
from flask import make_response, render_template, request

app = Flask(__name__)


@app.route("/set-expiring-cookie")
def set_expiring_cookie():
    """Set a new cookie that expires in 15 seconds."""
    response = make_response(render_template("template.html", cookies=request.cookies))
    response.set_cookie("expiring_cookie_name", "expiring_cookie_value", max_age=15)
    return response
```

The above route sets a cookie that expires after 15 seconds, even if the browser session is still active. What if we want a cookie to persist in the client's browser *forever*? It turns out we can't do that. The upper limit for `max_age` allowed by browsers is 400 days (approximately 13 months). The below Flask route function sets a cookie with an expiration of 400 days, the upper limit.

```python
from datetime import timedelta

from flask import make_response, render_template, request

app = Flask(__name__)


@app.route("/set-long-lasting-cookie")
def set_long_lasting_cookie():
    """Set a new cookie that expires in 400 days (the maximum mx_cookie age)."""
    response = make_response(render_template("template.html", cookies=request.cookies))
    response.set_cookie(
        "long_cookie_name", "long_cookie_value", max_age=timedelta(days=400)
    )
    return response
```

See that the `max_age` parameter also accepts a python `timedelta` object, making it easy to set a `max_age` in terms of days instead of manually calculating the equivalent in seconds.

What about the `expires` parameter? Yes, `response.set_cookie()` also accepts an `expires` parameter. `expires` is deprecated and no longer a recommended way to set cookie expirations. Instead, always use `max_age`. However, if you still want to use `expires`, pass a future date to `expires` to set a date when the cookie should expire.

## Cookie paths

It is possible to set a `path` value for cookies. A cookie `path` tells the client browser, "only send this cookie if the route matches *this* path". Let's look at an example:

```python
from flask import make_response, render_template, request

app = Flask(__name__)


@app.route("/set-path-cookie")
def set_path_cookie():
    """Set a new session cookie with the path value set.

    It will only be sent if the path matches the request path.
    It will match /set-path-cookie, /set-path-cookie/ and /set-path-cookie/anything
    """
    response = make_response(render_template("template.html", cookies=request.cookies))
    response.set_cookie(
        "path_cookie_name", "path_cookie_value", path="/set-path-cookie"
    )
    return response

```

As the function doc-string indicates, the above cookie, once set, will only be sent with requests that have a URL that start with `/set-path-cookie`, including `/set-path-cookie/` or `/set-path-cookie/*`, but not including something like `/set-path-cookie-alternate`. We can set the path as a parameter to `response.set_cookie`. The `path` provided to `response.set_cookie` matching the route used to set the cookie is purely coincidental.

Technically all cookies have a `path` parameter. However, the default path is `/` if `path` is not sent in the response, meaning send the cookie with *all* routes to the website. Why set a cookie `path`? Perhaps the cookie is only relevant to one area of the website. In this case, it is advantageous only to send the cookie when accessing this website area. Sending cookies costs bandwidth, so ideally, for maximum performance, they should be small and only sent when they will be actually *used*.

## Deleting cookies

To delete a cookie with Flask, call `response.delete_cookie(COOKIE_KEY)`, where COOKIE_KEY is the cookie's name (or key). Let's see an example:

```python
from flask import make_response, render_template, request

app = Flask(__name__)


@app.route("/delete-cookies")
def delete_cookies():
    """Delete all cookies we created."""
    response = make_response(render_template("template.html", cookies=request.cookies))
    response.delete_cookie("cookie_name")
    response.delete_cookie("path_cookie_name")
    response.delete_cookie("expiring_cookie_name")
    response.delete_cookie("long_cookie_name")
    return response
```

Notice we can call `response.delete_cookie()` as many times as desired. The above example will delete all cookies set by the other examples in this post.

## Conclusions

Cookies are key-value pairs of data stored on the *client's* browser, not on the server. They are useful for a variety of purposes, including session management. In the Python Flask framework, we can read cookies with the global `request` object. `request.cookies` is an immutable Python dictionary. We can generate a `flask.Response` object with `make_response()` passing in our rendered template. We can then call call `response.set_cookie()` to set new cookies or update existing cookies, and we can call `response.delete_cookie()` to delete cookies. Cookies, by default, expire when the current session ends, but we can set a different expiration using the `max_age` parameter. We can also set a path for the cookie with the `path` parameter.

Good luck using cookies to create awesome Flask applications! 🎉
