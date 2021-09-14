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
root. A `pre-commit` hook, is just an executable file with the magic name `pre-commit`
stored in this folder.

Note that some code editors make the `.git` folder hidden by default.
If you don't see it in your project root directory of your editor's file tree,
try playing around with your code editor's settings to make the `.git` folder
visible. For example in VS Code, type "Files: Exclude" into the "preferences"
menu see `.git` is hidden.

Once you can access your `.git` directory, open up the `.git/hooks/` directory.\
You will see a bunch of files named `hook-type.sample`.
You should see one named `pre-commit.sample`. If you open this file,
you will see an example pre-commit hook,
provided by git. You can use this as an actual pre-commit hook by simply
removing ".sample" from `pre-commit.sample`.
