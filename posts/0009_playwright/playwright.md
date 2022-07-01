# End-to-end webpage testing with Playwright

tags: testing, pytest, python, web

## Introduction

We all know testing your code is important, right? Automated tests can give you peace of mind that your code is working as expected and that it continues to work as expected, even as you refactor it. Python has the [pytest](pytest-url) framework that gives great tools for testing your python code. You can check out my blog post [9 pytest tips and tricks to take your tests to the next level](pytest-blog-post-url) to get yourself jump started testing in python. Javascript has several libraries to test your front-end code. But in website testing, how can we write automated tests to ensure that our back-end code (be it python or something else) is working with our front-end code (javascript, HTML, and CSS).

Introducing [Playwright](playwright-url), a fast, easy-to-use, and powerful end-to-end testing framework. This framework has tools that allow you to write tests that behave like real website users. And playwright has API endpoints in javascript, java, .NET, and **python**! Sound useful? Read on as we use Playwright with python and pytest to write end-to-end tests for our [Connect 4 game](connect-4 url).


