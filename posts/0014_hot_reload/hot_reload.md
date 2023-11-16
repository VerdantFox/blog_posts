# Hot reload FastAPI and Flask apps on HTML, CSS, and Javascript changes

tags: python, fastapi, flask, html, css, javascript, uvicorn, gunicorn, jinja2, browser-sync

## Introduction

01_HOT_RELOAD_INTRO_PIC

I love getting instant feedback for code changes when developing a web application. Typical workflows for Python web applications involve a _hot-reload_ functionality for the development web **server** that will restart the server when changes to **python** files are detected. However, the server will not restart when changes to **HTML**, **CSS**, or **JavaScript** files are detected. When those files are updated, you must manually restart the server for the changes to take place. Moreover, this typical workflow will not automatically refresh your web **browser** when you update files, so you must manually refresh the web page to see the changes.

In this tutorial, I'll show you how to **automatically** _hot-reload_ your FastAPI and Flask projects that use template engines like Jinja2 with uvicorn or gunicorn. You can automatically restart your server and refresh your browser when Python, HTML, CSS, and other files change.

## Example

You can find bare-bones example code for this tutorial in my GitHub repository named ["hot-reload-examples", here](https://github.com/VerdantFox/hot-reload-examples). The following GIF shows the example in action, using that repository's `fastapi` example.

02_HOT_RELOAD_VIDEO

## Installations

These are the installations you'll need to perform to get hot-reloads working.

### For both FastAPI and Flask

- NodeJS (google installation for your OS)
- npm (google installation for your OS)
- [browser-sync](https://browsersync.io/). The following command will install it globally.

  ```bash
  npm install -g browser-sync
  ```

### For FastAPI

- fastapi
- uvicorn[standard]
- jinja2

You can install these with `pip install fastapi "uvicorn[standard]" jinja2`.

### For Flask

- flask
- gunicorn

You can install these with `pip install flask gunicorn`.

## The steps

Here are the steps to get hot reloads working for your FastAPI or Flask project.

1. Run the server with `--reload`, specifying the files to look for when reloading.

   - `FastAPI` with `uvicorn`:

     ```bash
     uvicorn main:app --reload --reload-include="*.html" --reload-include="*.css" --reload-include="*.js"
     ```

     The above command will run a server on `http://localhost:8000` and watch for changes to Python files (default) and CSS, HTML, and JS files (according to the glob patterns we provided).

   - `Flask` with `gunicorn`:

     ```bash
     gunicorn main:app --reload --reload-extra-file="templates/index.html" --reload-extra-file="static/styles.css"
     ```

     The above command will run a server on `http://localhost:8000` and watch for changes to Python files (default), `templates/index.html`, and `static/styles.css`. Annoyingly, `gunicorn` currently does not allow you to specify glob patterns, so you must specify each non-python file to watch for changes.

   - Alternatively, you could run `Flask` with the Flask development server:

     ```bash
     flask --app main:app run --debug --extra-files templates/index.html:static/styles.css
     ```

     Use `;` on Windows to separate the `--extra-files` instead of `:`. The above command will run a server on `http://localhost:5000` and watch for changes to Python files (default), `templates/index.html`, and `static/styles.css`. Annoyingly, like with gunicorn, `flask` does not allow you to specify glob patterns, so you must specify each non-python file to watch for changes.

2. In a separate terminal, run [browser-sync](https://browsersync.io/) in watch mode, specifying the address to proxy and the static files path.

   ```bash
   browser-sync 'http://localhost:8000' 'static' --watch --files .
   ```

   Change the `localhost` port to the port your server is running on if it differs from `8000`. The above command will run a server on `http://localhost:3000` and proxy requests to `http://localhost:8000` (your server running FastAPI or Flask). It will also forward static files from the `static` directory (you can change the static files directory with the second argument to `browser-sync`). Finally, it will watch for changes to all files relative to the working directory and reload the browser when they change.

   Go to `http://localhost:3000`.

3. Turn off caching in your browser

   By default, browsers will cache static files. Therefore, you might not see changes to CSS and JavaScript files reflected in the browser, as the browser will use the stale cached after the first load. To fix this, you will need to turn off caching in your browser. For Chrome, you can do this with the following steps:

   1. Open the browser to `http://localhost:3000`
   2. Right-click on the browser page
   3. Click "Inspect" to open dev tools
   4. Navigate to the "Network" tab
   5. Check "Disable cache"

## Conclusion

After this tutorial, when developing your FastAPI or Flask application, you have the tools to change your Python, HTML, CSS, and Javascript files and see those changes will be reflected in the browser (`http://localhost:3000`) **automatically** without refreshing the page. Furthermore, the techniques shown here should work for any web application with built-in _hot-reload_ functionality--not just the two I showed examples for in this tutorial.
