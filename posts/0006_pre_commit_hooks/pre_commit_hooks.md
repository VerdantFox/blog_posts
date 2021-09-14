# How to use pre-commit hooks, the hard way and the easy way

tags: git, git hooks

## Introduction

GIT HOOK IMG

If you've heard of git `pre-commit` hooks, but you aren't really sure what
they are or how to get started with them, you are in luck! In this guide,
we'll talk about what git `pre-commit` hooks are and why you should consider
using them. We'll then talk about how to write your own git pre-commit hooks.
And finally, we'll talk about the *`pre-commit`* library which can make
setting up git `pre-commit` hooks a easy.

## What is a git pre-commit hook?

[Git hooks](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks){: target="_blank", rel="noopener noreferrer" }
in general, are scripts that get run when a specific event occurs in git.
They can be written in any language and do anything you like. The only requirement
for a git hook script is that it is an executable file.

What events in git can trigger a git hook?
Git hook events can trigger on the server side (where the code is stored remotely
-- GitHub, GitLab, etc.) or locally (on your computer). Local git events that can
trigger a hook script to run include:

- `pre-commit` (occurs before a git commit is accepted)
- `post-commit` (occurs immediately after a git commit is accepted)
- `post-checkout` (occurs before a git checkout)
- `pre-rebase` (occurs before a git rebase)

There are several other local git hook triggers, and also several server side
git hook triggers. But for this guide, we're specifically going to be talking
about `pre-commit` hooks. What is special about the `pre-commit` hook?
This hook runs when you run the command `git commit`. The hook runs *before*
a commit is accepted to git, and if the hook script fails (ie if it returns a
non-zero exit code) the commit is aborted. This is *powerful*! It means
you can automatically run
[linters](https://sourcelevel.io/blog/what-is-a-linter-and-why-your-team-should-use-it){: target="_blank", rel="noopener noreferrer" }
to statically analyze your code and make sure it is high quality and syntax-error
free before the code is committed. If your code doesn't meet your quality standards,
your commit will be rejected (for now). You can get told what, specifically,
needs fixing, and in some cases you could have your code fixed for you on the
spot.

## How to write your own git pre-commit hook (the hard way)

Now that we know *what* a git `pre-commit` hook is, *how* can we write one?
All git hooks are stored in the `.git/hooks/` directory under your project
root. A `pre-commit` hook, is just an executable file stored in this folder
with the magic name `pre-commit`.

Note that some code editors make the `.git` folder hidden by default.
If you don't see it in your project root directory of your editor's file tree,
try playing around with your code editor's settings to make the `.git` folder
visible. For example in VS Code, type "Files: Exclude" into the "preferences"
menu see `.git` is hidden.

Once you can access your `.git` directory, open up the `.git/hooks/` directory.
You will see a bunch of files named `hook-type.sample`.
You should see one named `pre-commit.sample`. If you open this file,
you will see an example pre-commit hook,
provided by git. You can use this as an actual pre-commit hook by simply
removing ".sample" from `pre-commit.sample`. The sample pre-commit hook
is a bit confusing. Lets write our own, more straightforward hook.

Example pre-commit hook for a python project:

```bash
#!/usr/bin/env bash
# ^ Note the above "shebang" line. This says "This is an executable shell script"
# Name this script "pre-commit" and place it in the ".git/hooks/" directory

# If any command fails, exit immediately with that command's exit status
set -eo pipefail

# Run flake8 against all code
flake8 source_code
echo "flake8 passed!"

# Run black against all code
black source_code --check
echo "black passed!"
```

The above `pre-commit` hook, when placed in the `.git/hooks/` directory,
will first run when you perform a `git commit`. First,
[flake8](https://flake8.pycqa.org/en/latest/){: target="_blank", rel="noopener noreferrer" }
will scan your python code for its style requirements and then
[black](https://black.readthedocs.io/en/stable/){: target="_blank", rel="noopener noreferrer" }
will scan your python code for its style requirements.
These are two awesome python code linters I highly recommend you add to
any python project. If either of these python linters fail, your
commit will abort with a message from the failed linter. Once you fix
those errors and try to commit again, the script will succeed and exit with
status code 0, and then your commit will succeed.

As I stated earlier, `pre-commit` hooks are very flexible. The above script was
written in `bash`, but the script could have
been written in `python`, `ruby`, `node JS`, or any other scripting language.
Furthermore, the script could call other scripts in your code. This is a great
way to chain together lots of hooks into one file. Simply write a base
`pre-commit` hook script, that calls all of your other `pre-commit` hook
scripts you want to run. Those scripts could also run in any language, or
even start docker containers that perform checks or make changes for you.
Finally, these scripts can even modify your code for your on the spot. If you
do modify your code in a `pre-commit` script, make sure to exit with a
non-zero exit status. Changes made won't be staged, and thus won't be
committed (plus you might want to view those changes before re-committing).

You are now equipped to write your own custom `pre-commit` hooks. But there
is an easier way! In the next section, we'll discuss the
[`pre-commit`](https://pre-commit.com/){: target="_blank", rel="noopener noreferrer" }
framework, which can make managing pre-commit scripts much easier.

## The `pre-commit` framework. `pre-commit` scripts the easy way!

PRE-COMMIT LOGO
