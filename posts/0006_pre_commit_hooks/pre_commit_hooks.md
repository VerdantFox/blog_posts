# How to use pre-commit hooks, the hard way, and the easy way

tags: git, git hooks

## Introduction

GIT HOOK IMG

If you've heard of git pre-commit hooks, but you aren't sure what
they are or how to get started with them, you are in luck! In this guide,
we'll talk about what git pre-commit hooks are and why you should consider
using them. We'll then talk about how to write your own git pre-commit hooks,
and then we'll talk about the `pre-commit` framework which can make
setting up git pre-commit hooks easy.

## What is a git pre-commit hook?

[Git hooks](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks){: target="_blank", rel="noopener noreferrer" }
in general, are scripts that get run when a specific event occurs in git.
They can be written in any language and do anything you like. The only requirement
for a git hook script is that it is an executable file.

What events in git can trigger a git hook?
Git hook events can trigger on the server-side (where the code is stored remotely
-- GitHub, GitLab, etc.) or locally (on your computer). Local git events that can
trigger a hook script to run include:

- `pre-commit` (occurs before a git commit is accepted)
- `post-commit` (occurs immediately after a git commit is accepted)
- `post-checkout` (occurs before a git checkout)
- `pre-rebase` (occurs before a git rebase)

There are several other local git hook triggers, and also several server-side
git hook triggers. But for this guide, we're specifically going to talk
about git pre-commit hooks. What is special about the pre-commit hook?
This hook runs when you run the command `git commit`. The hook runs *before*
a commit is accepted to git, and if the hook script fails (ie if it returns a
non-zero exit code) the commit is aborted. This is *powerful*! It means
you can *automatically* run
[linters](https://sourcelevel.io/blog/what-is-a-linter-and-why-your-team-should-use-it){: target="_blank", rel="noopener noreferrer" }
to statically analyze your code and make sure it is high quality and syntax-error-free
*before* the code is committed. If your code doesn't meet your linters' quality standards,
your commit will be rejected (for now). Your linters will tell you what,
specifically, needs fixing, and in some cases, you can have your code fixed
automatically, on the spot.

## How to write a git pre-commit hook (the hard way)

Now that we know *what* a git pre-commit hook is, *how* can we write one?
All git hooks are stored in the `.git/hooks/` directory under your project
root. A pre-commit hook is just an executable file stored in this folder
with the magic name `pre-commit`.

Note that some code editors make the `.git/` folder hidden by default.
If you don't see it in your project root directory of your editor's file tree,
try playing around with your code editor's settings to make the `.git/` folder
visible. For example, in VS Code, type "Files: Exclude" into the "preferences"
menu to see `.git/` is hidden.

Once you can access your `.git/` directory, open up the `.git/hooks/` directory.
You will see a bunch of files named `hook-type.sample`.
You should see one named `pre-commit.sample`. If you open this file,
you will see an example pre-commit hook,
provided by git. You can use this as an actual pre-commit hook by simply
removing ".sample" from `pre-commit.sample`. The provided sample pre-commit hook
is a bit confusing. Let's write our own, more straightforward hook.

*Example pre-commit hook for a python project:*

```bash
#!/usr/bin/env bash
# ^ Note the above "shebang" line. This says "This is an executable shell script"
# Name this script "pre-commit" and place it in the ".git/hooks/" directory

# If any command fails, exit immediately with that command's exit status
set -eo pipefail

# Run flake8 against all code in the `source_code` directory
flake8 source_code
echo "flake8 passed!"

# Run black against all code in the `source_code` directory
black source_code --check
echo "black passed!"
```

The above pre-commit hook, when placed in the `.git/hooks/` directory,
will run when you perform a `git commit` command. First,
[flake8](https://flake8.pycqa.org/en/latest/){: target="_blank", rel="noopener noreferrer" }
will scan your python code for its style requirements, and then
[black](https://black.readthedocs.io/en/stable/){: target="_blank", rel="noopener noreferrer" }
will scan your python code for its style requirements.
These are two awesome python code linters I highly recommend you add to
any python project. If either python linter fails, the script will immediately
exit with a non-zero status code (due to `set -eo pipefail`). Therefore, your
commit will abort with a message from the failed linter. Once you fix
those errors and try to commit again, the script will succeed and exit with
status code `0`, and then your commit will succeed.

The above pre-commit hook script is a nice start. But note, we can also call git
commands in a hook script. Therefore, we can see specifically which files
are to be committed in this commit and only run our linters against those
files. How might that look?

*Modified pre-commit script that only runs against modified files:*

```bash
#!/usr/bin/env bash

# If any command fails, exit immediately with that command's exit status
set -eo pipefail

# Find all changed files for this commit
# Compute the diff only once to save a small amount of time.
CHANGED_FILES=$(git diff --name-only --cached --diff-filter=ACMR)
# Get only changed files that match our file suffix pattern
get_pattern_files() {
    pattern=$(echo "$*" | sed "s/ /\$\\\|/g")
    echo "$CHANGED_FILES" | { grep "$pattern$" || true; }
}
# Get all changed python files
PY_FILES=$(get_pattern_files .py)

if [[ -n "$PY_FILES" ]]
then
    # Run black against changed python files for this commit
    black --check $PY_FILES
    echo "black passes all altered python sources."
    # Run flake8 against changed python files for this commit
    flake8 $PY_FILES
    echo "flake8 passed!"
fi
```

As I stated earlier, pre-commit hooks are very flexible. We wrote the above
scripts in `bash`, but the scripts could have
been written in `python`, `ruby`, `node JS`, or any other scripting language.
Furthermore, a script can call other scripts in your code. This is a great
way to chain together lots of hooks into one file. Simply write a base
pre-commit hook script that calls all of your other pre-commit hook
scripts. Those scripts could also run in any language, or
even start docker containers that perform checks.
Finally, these scripts can even modify (fix) your code as they run. If you
do modify your code in a pre-commit script, make sure to exit with a
non-zero exit status. Changes made won't be staged, and thus won't be
committed (plus you might want to view those changes before re-committing).

You are now equipped to write your own custom pre-commit hooks. But there
is an easier way! In the next section, we'll discuss the
[pre-commit](https://pre-commit.com/){: target="_blank", rel="noopener noreferrer" }
framework, which can make managing pre-commit scripts much easier.

## The pre-commit framework (pre-commit scripts made easy)

PRE-COMMIT LOGO

The [pre-commit](https://pre-commit.com/){: target="_blank", rel="noopener noreferrer" }
framework bills itself as "A framework for managing and maintaining
multi-language pre-commit hooks." Under the hood, it runs on python,
but you can use the framework on any project, regardless of your project's primary
language. Once installed, you're going to add a `pre-commit` configuration file to
your project root named `.pre-commit-config.yaml`. In that config file,
you will specify which scripts `pre-commit` will run when your pre-commit
hook is triggered by a `git commit` command. Additionally, you can run
the pre-commit scripts any time outside of a `git commit` call -- more on that later.
The configuration file will look something like *this* (example taken from
the pre-commit documentation):

*Example `.pre-commit-config.yaml` file:*

```yaml
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v2.3.0
    hooks:
    -   id: check-yaml
    -   id: end-of-file-fixer
    -   id: trailing-whitespace
-   repo: https://github.com/psf/black
    rev: 19.3b0
    hooks:
    -   id: black
```

The above file specifies that 4 scripts will run:

- `check-yaml` (lints yaml file syntax)
- `end-of-file-fixer` (makes sure files end in a newline and only one newline)
- `trailing-whitespace` (trims trailing whitespace)
- `black` (checks and fixes python code style)

The first 3 scripts were pulled from the repository
<https://github.com/pre-commit/pre-commit-hooks> and the last script was pulled
from the repository <https://github.com/psf/black>. For each repository, you
must specify a `rev` (revision) which makes sure the script behaves according
to that revision instead of always updating to the latest. Pre-commit scripts
from these remote repositories can be written in any language. All of their
requirements are specified in their repository. The `pre-commit` framework will
read those requirements and build an appropriate environment to run that script.
This might mean `pre-commit` will install a specific python version for an
isolated environment to run `black`, or it might mean `pre-commit` will install
a specific `npm` package in an isolated environment to run a `node` script.
This is great for you, the developer since you don't have to prepare any of
these special environments yourself, and it means you can use any script that
is useful to you, regardless of the language it is written in.

Once you have the `pre-commit` framework installed and your
`.pre-commit-config.yaml` file is ready, run `pre-commit install` to install/set up
the hooks specified in your configuration file. At this point, `pre-commit`
is ready to go and will automatically run when `git commit` is called.
For most hooks, this means running
*specifically against files updated by your git commit*. You can also run
`pre-commit run --all-files` at any time to run your pre-commit hooks
against *all files in your repository*. I highly suggest running this command
immediately after any `pre-commit install` to fix all of your
files according to your installed hooks.

## Finding supported pre-commit hooks and rolling your own hooks

Where can you find `pre-commit`-framework-ready repositories/hooks
to use in your `.pre-commit-config.yaml` file?
[Check out this list of supported hooks maintained by pre-commit](https://pre-commit.com/hooks.html){: target="_blank", rel="noopener noreferrer" }.
There are a *lot* of repositories with hooks compatible
with the `pre-commit` framework. Browse the list to see if your favorite
tool has a supported hook. When you click on a repository, read through
its documentation on its pre-commit hook. It will likely tell you exactly
how to format its section of the `.pre-commit-config.yaml` file.

What if you can't find a supported pre-commit hook for your lint tool-of-choice
or what if you want to run a project-specific custom script during `pre-commit`?
Fear not! `pre-commit` allows for this. This use case is documented in
"[Repository local hooks](https://pre-commit.com/#repository-local-hooks){: target="_blank", rel="noopener noreferrer" }".
To summarize, a `local` hook must define `id`, `name`, `language`, `entry`, and `files`/`types`.
I found that it is simplest to define `id` and `name` as the same thing.
`files` or `types` refer to either the specific files or the type of files
to check for and run the script against.
I also found that the easiest way to get custom hooks to work is to set the `language` to
`script` with an `entry` pointing at a local script (`./your/script/location`) relative
to your project root. In this case, no special environment will be created
by `pre-commit install`, so you will need to have your local environment already
appropriately set up to run the script (for instance have the correct version
and packages of `python`, `npm`, etc, installed on your local system).
Note that `pre-commit` will run your custom script against every file matched
by `files`/`types` individually, so design your script accordingly.

Here is an example configuration with a few `local` hooks, taken directly
from `pre-commit`'s documentation on this subject:

```yaml
-   repo: local
    hooks:
    -   id: pylint
        name: pylint
        entry: pylint
        language: system
        types: [python]
    -   id: check-x
        name: Check X
        entry: ./bin/check-x.sh
        language: script
        files: \.x$
    -   id: scss-lint
        name: scss-lint
        entry: scss-lint
        language: ruby
        language_version: 2.1.5
        types: [scss]
        additional_dependencies: ['scss_lint:0.52.0']
```

## Conclusions

In this post, first, we answered the question
"[What is a git pre-commit hook?](#what-is-a-git-pre-commit-hook)".
We touched on what git hooks are in general and how the pre-commit hook
fits into other hooks. We discussed how the pre-commit hook is triggered,
what happens when it is triggered, and why pre-commit hooks are awesome. Then we discussed
"[how to write a git pre-commit hook (the hard way)](#how-to-write-a-git-pre-commit-hook-the-hard-way)".
We talked about where pre-commit hooks live, and how to write them
with examples. Next, we talked about
"[the pre-commit framework (pre-commit scripts made easy)](#the-pre-commit-framework-pre-commit-scripts-made-easy)".
We discussed why the `pre-commit` framework is awesome and easy to use, and we saw an example
of how to set up some hooks using the framework. Finally, we discussed
"[where to find supported pre-commit hooks and rolling your own hooks](#finding-supported-pre-commit-hooks-and-rolling-your-own-hooks)".
We discussed how to get supported pre-commit hooks from remote repositories,
and in cases where that's not possible, we discussed how to add your own
scripts and custom hooks to your `.pre-commit-config.yaml` file.

I hope you enjoyed this introduction to pre-commit hooks, and I hope it
helps you get started using pre-commit hooks in your code. If you
were already familiar with pre-commit hooks but hadn't heard about the
`pre-commit` framework, I hope you're excited to give the framework a try.
Happy coding!
