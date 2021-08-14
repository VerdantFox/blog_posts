# My top 20 VS Code extensions awesome list

tags: vscode, editors, awesome lists

## Introduction

IMAGE: 00_vs_code.png

Microsoft released VS Code (VisualStudio Code) in 2015, and since then
it has become one of the most popular text editors on the market. What has
led to that popularity? It is **free** and lightweight, with a beautiful and
intuitive user interface and it is fully customizable through **extensions**.
Extensions can bring nearly any look or functionality you like to VS Code.
But with so many extensions to choose from, which ones are right for *you*?
I'm here to guide you with my top 20 favorite VS Code extensions.

## 1. Project Manager

IMAGE: 01_project_manager.png

Do you work on several projects and find yourself switching back and forth
all the time between them. Then this is the perfect extension for you.
The `Project Manager` extension easily tops this list as one of my all-time
favorite extensions.

Once downloaded, a new folder tab icon will appear on the
left-hand side of your VS Code editor. Whenever you start a new
project, open this tab and hit the "save project" icon at the top of the
left-hand panel. `Project Manager`  will add your project to a list
of your favorite projects.

In the future, if you ever want to return to this project, open up
this panel and left-click your project to jump to it. You can also right-click
a project to open that project in a new window. This functionality is very
convenient if you like to reference code from previous projects when
starting a new project.

## 2. GitLens

IMAGE: 02_gitlens.png

GitLens helps you examine the commit history for a line of code.
Click on a line of code, and off to the right-hand side, you will see
an un-obtrusive git blame message. The message will contain
(1) **who** last changed that line of code, (2) **when** they changed it, and
the (3) **what** the commit message said for that change.
If you then hover that git blame segment, you'll have options to pull
up a `diff` with all the changes made to the current file for that commit,
pull up the commit in `GitHub` or `GitLab`, and other options.

## 3. Open in Browser

IMAGE: 03_open_in_browser.png

This simple extension allows you to easily open an HTML file in the browser.
You can right-click the file itself in the left-hand file browser or right-click
in the opened HTML file itself. You'll have the option to
"Open in Default Browser" or "Open in Other Browsers". Supported browsers are
`Chrome`, `Firefox`, and `Opera`.

## 4. Code Spell Checker

IMAGE: 04_code_spell_checker.png

I type fast and frequently make small spelling mistakes.These mistakes often used to go
unnoticed until a co-worker pointed them out in code review. Well, no more!
As the name suggests, `Code Spell Checker` checks your code for spelling mistakes.
And not just spelling mistakes in comments, but in variable names, function names,
and class names as well. It is smart about word tokenizing on `snake_case` and `camelCase`
code. `Code Spell Checker` underlines misspelled words. If you click the
underlined word, a lightbulb will appear on the left side of your screen
with suggestions for words with similar spellings. And if you right-click
the word, you can tell the extension to add the word to the dictionary
or to ignore the word for now.

## 5. Bracket Pair Colorizer

IMAGE: 05_bracket_pair_colorizer.png

This nifty extension will color `[square brackets]`, `{curly braces}`, and
`(parentheses)` colors that match on the left and right sides.
Inner brackets get different colors than the outer brackets. This
coloring makes it so quick and easy to tell which brackets align on the
left and right sides, and makes it very easy to tell when you're missing
a closing bracket.

## 6. Toggle Quotes

IMAGE: 06_toggle_quotes.png

`Toggle Quotes` is a fun, little extension that allows you to
toggle back-and-forth between double-quotes and single-quotes. Just put your
blinking cursor inside the quotes to change and press `Ctrl+'`.

## 7. Copy Relative Path Posix

IMAGE: 07_copy_relative_path_posix.png

If you are like me and you work on a `Windows` machine but use `git-bash` or
have a project with file paths that need forward-slashes, and you need your
copied file paths to also have forward slashes, `Copy Relative Path Posix`
will save you so much time. If you right-clicking a file in the left-hand file
browser, in addition to the standard "Copy Path" and "Copy Relative Path",
there will now be an option to "Copy Relative Path (Posix)". This option will
copy the file path relative to your project root, but with forward-slashes
instead of backslashes.

## 8. Auto Close Tag

IMAGE: 08.1_auto_close_tag.png
IMAGE: 08.2_auto_close_tag.png

`Auto Close Tag` is an extension that automatically places closing tags on
HTML and XML tags. Just type an opening tag, and as soon as you type the
`>` to finish the tag, the extension will create a matching closing tag
and place your cursor between the opening and closing tags. It is also smart
enough to know certain tags that should not receive a closing tag
(such as `<br>`), and you can extend that list of non-closed tags.

## 9. Auto Rename Tag

IMAGE: 09.1_auto_rename_tag.png
IMAGE: 09.2_auto_rename_tag.png

`Auto Rename Tag` recognizes a pair of opening and closing HTML or XML tags.
If you edit the opening tag from that pair, it will change the closing tag to match.
For example, if you replace `h2` with `p` from your opening tag, the extension
will change the closing tag at the same time. So `<h2>Some text</h2>` becomes
`<p>Some text</p>` without you having to find the closing tag and change
it yourself.

## 10. Highlight Matching Tag

IMAGE: 10_highlight_matching_tag.png

As with brackets, it can be difficult to match an opening HTML or XML tag
to its closing tag, especially when there is a lot of nested code in between
the two. `Highlight Matching Tag` simply highlights (with a yellow underline)
the opposing closing tag when your blinking cursor is on an opening tag or
the opposing opening tag when your blinking cursor is on a closing tag, making
it so you can find one or the other with ease.

## 11. Color Highlight

IMAGE: 11_color_highlight.png

`Color Highlight` highlights all CSS color codes in your codebase the color
they represent. So if I write `#fff` in my code (in any file, not just a `CSS`
file), that `#fff` block of code is colored white. This coloring also works
with RGB colors like `rgb(255, 255, 255)`, or named colors like `pink`. The
named colors, however, will only highlight their respective color in a
CSS file. This extension is great for easily seeing what colors look like
inline in your code. I certainly don't memorize (most) hex codes and would have
no idea what `#af1` corresponds to without looking it up or without this
extension.

## 12. Path Intellisense

IMAGE: 12.1_path_intellisense.png
IMAGE: 12.2_path_intellisense.png
IMAGE: 12.3_path_intellisense.png

`Path Intellisense` knows your file tree. When you open a file and start typing
a path inside a set of quotation marks, `Path Intellisense` will suggest
options for the next directory or file in the path. You can then press
`tab` or `enter` to add the suggestion to the path you are typing. It can
detect paths relative to the current file with `./relative/path/notation`
or relative to the project root with `/absolute/path/notation`.

## 13. vscode-faker

IMAGE: 13.1_vscode-faker.png
IMAGE: 13.2_vscode-faker.png
IMAGE: 13.3_vscode-faker.png

`Vscode-faker` is an awesome extension for adding fake data to your file.
Press `Ctrl+Shift+P` to open the VS Code command bar, then type `faker`.
The dropdown menu will populate with a whole list of data categories
to fake out including **names**, **phone numbers**, **email addresses**,
**vehicles**... the list goes on and on. One of the most useful fakes for me
is the `Faker: Lorem`, which you can use to generate paragraphs of `lorem ipsum`
to fill your HTML pages out with to see how they look before you replace
that `lorem ipsum` with real content. Once an item-to-fake is selected,
it will appear in the file at your cursor.

## 14. Prettier - Code formatter

IMAGE: 14.1_prettier.png
IMAGE: 14.2_prettier.png

`Prettier` is a code formatter that supports a wide range of file types
including `HTML`, `CSS`, `Javascript`, `Markdown`, and several others.
Once installed, you can right-click anywhere in a supported file and
select the option `Format Document` to have `Prettier` automatically
format your code in a consistent, easy-to-read format.

## 15. CSS Peek

IMAGE: 15_css_peek.png

`CSS Peek` adds `Go To Definition` functionality to your `HTML` classes.
While in an HTML file, hold `Ctrl` while hovering a custom `CSS` class
to see a pop-up of the `CSS` class above your hovered cursor position.
You can then click said `CSS` class to go to its definition in the
`CSS` file for easy editing.

## 16. Sourcery

IMAGE: 16.1_sourcery.png
IMAGE: 16.2_sourcery.png
IMAGE: 16.3_sourcery.png
IMAGE: 16.4_sourcery.png

`Sourcery` is a cool extension for `python`. It finds patterns in
your opened python file that could be refactored to be made clearer,
and it underlines the affected code. If you hover over the underlined code,
`Sourcery` will tell you (in a pop-up below your cursor) what should be
refactored. It also shows you what the refactored code would look like
compared with the current code in a `diff` within the pop-up.
If you then left-click the underlined code, a lightbulb
will appear on the left-hand side of the screen with an option for `Sourcery`
to change your code to its suggested refactoring. If you disagree with the
suggested refactoring, there are options to skip this instance of the
refactoring or even tell `Sourcery` never to show the suggested type of
refactoring again.

While the extension is great for everyone, it is especially awesome for
beginner python developers as it can point out un-pythonic patterns in their
code to make them better developers in the future.

## 17. flask-snippets

IMAGE: 17.1_flask-snippets.png
IMAGE: 17.2_flask-snippets.png

`Flask-snippets` provides shortcuts for `Flask` and `jinja` code patterns.
On the `Flask` side of things, you can start typing `fapp`, and as you type,
a completion suggestion will appear for `fapp` which you can select by
pressing `Tab` or `Enter`. This will generate the following code for you:

```python
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
```

The above code is the code for a basic `Flask` application. You can also
start typing `froute` to generate a basic `Flask` route that looks like this:

```python
@app.route('path')
def func_name(foo):
    return render_template('expression')
```

There are 18 such basic flask snippets for quick code completion
that you can see by going to the `flask-snippets` extension page. While those
flask snippet code completions are helpful, the completions I find most helpful
are for `jinja` template code completions. With an `HTML` `jinja` file open,
start typing `ffor` to get the following code completion snippet:

```jinja
{% for element in collection %}
    {{ element|e }}
{% endfor %}
```

Or start typing `felif`  in an `HTML` `jinja` file to get the following code:

```jinja
{% if expression %}
    blockofcode
{% elif expression2 %}
    blockofcode
{% else %}
    blockofcode
{% endif %}
```

There are 17 such `jinja` template code completion snippets which I find to
be great time savers. And while `jinja` templates are used extensively by
`Flask`, other web frameworks (such as `FastAPI`) can also make use of
`jinja` templates, making this extension very useful when working on those
web frameworks as well.

## 18. Language support

IMAGE: 18_language_support_bash_IDE.png

These last three extensions aren't really `extensions` so much as they are categories
of extensions. This category is all about language support extensions. VS Code
is great for working with any programming language under the sun because
most likely any language you want to code with has a VS Code language support
extension for it with features like `code completion`, `go to definition`,
`syntax error highlighting`, etc. This support makes it so much easier to
write new code, understand old code, and spot syntax errors in your code quickly.
For the language you are interested in working with, just type that language
into the extension search bar and the first hit will probably be language support for that
language. Here is a list of the languages I use all the time alongside
their supporting extensions:

- Markdown ==> `markdownlint` + `Markdown All in One`
- HTML and CSS ==> `HTML CSS support`
- Jinja ==> `Jinja`
- Python ==> `Python`
- YAML ==> `YAML`
- Bash ==> `Bash IDE` (this is shown in the above picture)

## 19. Color Themes

IMAGE: 19_themes_one_dark_pro.png

VS Code can look exactly the way you like with `color themes`. While
color themes are just `extensions` and can be installed just like any other
extension, the more typical way to install a color theme is by going to
`File > Preferences > Color Theme`. From this drop-down, you can scroll up
and down in the color themes with your keyboard arrows. Your VS Code
will instantly switch to the highlighted theme so you can quickly find what
looks good to you. Note that these default themes are a limited selection.
To get a fuller picture of the themes available you can browse themes at
<https://vscodethemes.com/>{: target="_blank", rel="noopener noreferrer" }.
I am personally quite partial to `One Dark Pro`.

## 20. Icon themes

IMAGE: 20_icon_themes_material_icon_theme.png

The other cool place you can customize your VS Code visual experience is with
`icon themes`. Icon themes transform the icons in the left-hand file
browser, making them "pop" a little more (or less). While the default theme
for VS Code icons (called `Seti`) is pretty nice looking, it's
worth giving other icon themes a chance. The easiest way to find icon themes is
by going to the extensions panel and typing `icon theme` into the search
bar. Then, scroll through and click on a few of the options to see how their
icons look on their description pages. I picked up the `material icon theme`.
This theme supports just about any file extension out there and makes it easy for
me to distinguish between various file types and important folder types.

## Conclusions

VS Code is an awesome, fast, and lightweight text editor. With extensions,
you can customize it to look and behave just about any way you like. I hope
you liked my picks for my top 20 favorite VS Code extensions, and maybe you
found a couple of new ones to pick up for yourself. Did I miss any VS Code
extensions that *you* truly love? I'd love to hear about them in the comments
below!
