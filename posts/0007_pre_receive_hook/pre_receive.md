# How to write a git pre-receive hook and install it in gitlab

tags: git, git hooks

## Introduction

GIT HOOK IMG

In the last blog post
[we talked about git pre-commit hooks](https://verdantfox.com/blog/view/how-to-use-git-pre-commit-hooks-the-hard-way-and-the-easy-way){: target="_blank", rel="noopener noreferrer" }.
In this article we'll discuss git *pre-receive* hooks -- what they are,
why they are useful, how to write them, and how to install them on a gitlab
server.

## What is a git pre-receive hook?

For a refresher on git hooks in general, check out the last post,
[How to use git pre-commit hooks, the hard way and the easy way](https://verdantfox.com/blog/view/how-to-use-git-pre-commit-hooks-the-hard-way-and-the-easy-way){: target="_blank", rel="noopener noreferrer" }.
The pre-receive git hook is a server-side script that runs when the
server receives a commit from your `git push` command (or from server-generated
commits like those created by GitLab or GitHub). Once installed, the hook
script will run just *before* a commit is accepted. If the script succeeds
(if it returns an exit code of `0`), the commit is accepted. If the script
returns a non-zero exit code, the commit is rejected.

Why is a pre-receive hook useful? Recall, client-side hooks like the pre-commit
hook, are installed on a developer's local machine. A team can ask developers
to install client side hooks to check their code or commit messages,
but it's hard to enforce that practice. Furthermore, its possible for developers'
client-side hooks to get out-of-sync with each other. Because the pre-receive hook
script runs on the remote server and can reject commits, it allows an team to
enforce coding practices on the entire team without relying on individual
members to install the hooks and keep them up to date.

Something to note about remote server git hooks like the pre-receive hook.
Such hooks can only be installed on privately owned servers. For instance,
we installed a pre-receive hook on our company-owned GitLab server. You
could also install such a hook on a private GitHub enterprise server or
a private BitBucket server. It is not possible to install such a script for
a github repository at <github.com>. This is because these scripts run
arbitrary code and so must be trusted by the server administrator not to
container malicious code.

## Example pre-receive hook

Lets take a look at an example pre-receive hook that enforces a commit
message style on merges to the `main` (or `master` branch) branch.
The hook is written for a hypothetical team with the the Jira ticket
id of "ABC". I wrote a pre-receive script
very similar to this one that our team actually uses for our project.
The hook script is written in `bash` because `bash` is widely available
on most linux systems and so would be available on our `GitLab` server, but
it could have been written in any language, so long as the server can
understand that language.
First I'll show the code in its entirety, then we'll break down what is
happening in each section.

pre-receive hook to enforce commit message style for the ABC team:

```bash
#!/usr/bin/env bash
#
# `pre-receive` hook to enforce commit messages follow
# ABC project commit standard style.


# If any command fails, exit immediately with that command's exit status
set -eo pipefail

MAIN_BRANCH="refs/heads/main"  # Switch to 'refs/heads/main' if your main branch is named 'master'
MAX_LINE_LENGTH=100
COMMIT_REGEX='^(build|ci|docs|feat|fix|perf|refactor|style|test)\([a-z_,]+\)!?:\ [a-zA-Z].+\ \[ABC-[0-9]+\](
[A-Z#].*)?$'

# Check commit message matches ABC commit style
function check_msg_style
{
    msg="$1"
    if ! [[ "$msg" =~ $COMMIT_REGEX ]]
    then
        echo "GL-HOOK-ERR: Commit message DOES NOT follow ABC commit style."
        echo "GL-HOOK-ERR: Output should look as follows:"
        echo "GL-HOOK-ERR: \`\`\`"
        echo "GL-HOOK-ERR: type(scope): jira ticket title [ABC-1234]"
        echo "GL-HOOK-ERR: (empty line if writing description)"
        echo "GL-HOOK-ERR: Optional merge request description."
        echo "GL-HOOK-ERR: \`\`\`"
        echo "GL-HOOK-ERR: Possible types: build, ci, docs, feat, fix, perf, refactor, style, test"
        echo "GL-HOOK-ERR: 'scope' generally refers to which part of the codebase is changing (ie a module or package)."
        exit 1
    fi
}
# Check that lines do not exceed character limit
function check_msg_line_lengths
{
    msg="$1"
    IFS=$'\n' lines=("$msg")
    for line in ${lines}
    do
        string_length=${#line}
        if [[ $string_length -gt $MAX_LINE_LENGTH  ]]
        then
            echo "GL-HOOK-ERR: Commit message contains one or more lines longer than ${MAX_LINE_LENGTH} characters."
            echo "GL-HOOK-ERR: First line that exceeds character limit:"
            echo "GL-HOOK-ERR: ${line}"
            exit 2
        fi
    done
}

while read line
do
    # Only if line is not empty.
    if [[ -n "${line// }" ]]; then
        # Split the line into array.
        IFS=' ' read -r -a array <<< "$line"
        # This is the standard Git behavior for pre-receive:
        parent_sha=${array[0]}
        current_sha=${array[1]}
        ref=${array[2]}
        # Exit with success if push is not to `main` branch
        if [[ "$ref" != "$MAIN_BRANCH" ]]; then
            exit 0
        fi
        # Should only be one item in rev-list if this is a squash commit
        for commit in $(git rev-list "${parent_sha}".."${current_sha}"); do
            commit_msg="$(git cat-file commit "${commit}" | sed '1,/^$/d')"
            check_msg_style "$commit_msg"
            check_msg_line_lengths "$commit_msg"
        done
    fi
done < "${ST:-/dev/stdin}"

# Success! Squash commit meets ABC commit style.
exit 0
```

Alright, let's break down what is happening in these ~75 lines of `bash` code.

```bash
#!/usr/bin/env bash
```

↑ The first line of the script is the "shebang" line. It tells the server
reading this script that it is a bash script and should be interpreted as such.

```bash
set -eo pipefail
```

↑ This line tells the script to exit immediately if any individual command
in the script fails and set the script's exit code to that command's exit code.

```bash
MAIN_BRANCH="refs/heads/main"  # Switch to 'refs/heads/main' if your main branch is named 'master'
MAX_LINE_LENGTH=100
COMMIT_REGEX='^(build|ci|docs|feat|fix|perf|refactor|style|test)\([a-z_,]+\)!?:\ [a-zA-Z].+\ \[ABC-[0-9]+\]$'
```

↑ Here we set some global variables for the script. The `MAIN_BRANCH` variable
specifies the name of our `main` branch. For new projects this branch name is
usually `main`. For older projects this branch name is usually `master`.
`MAX_LINE_LENGTH=100` specifies that we don't want any line in the commit
to exceed 100 characters. `COMMIT_REGEX` specifies a regular expression
that lays out the style we want all commits to follow.

```bash
# Check commit message matches ABC commit style
function check_msg_style
{
    msg="$1"
    if ! [[ "$msg" =~ $COMMIT_REGEX ]]
    then
        echo "GL-HOOK-ERR: Commit message DOES NOT follow ABC commit style."
        echo "GL-HOOK-ERR: Output should look as follows:"
        echo "GL-HOOK-ERR: \`\`\`"
        echo "GL-HOOK-ERR: type(scope): jira ticket title [ABC-1234]"
        echo "GL-HOOK-ERR: (empty line if writing description)"
        echo "GL-HOOK-ERR: Optional merge request description."
        echo "GL-HOOK-ERR: \`\`\`"
        echo "GL-HOOK-ERR: Possible types: build, ci, docs, feat, fix, perf, refactor, style, test"
        echo "GL-HOOK-ERR: 'scope' generally refers to which part of the codebase is changing (ie a module or package)."
        exit 1
    fi
}
```

↑ This bash function has a simple `if` statement. It receives a commit message
as an argument. If that commit message doesn't match the `COMMIT_REGEX` regular
expression we specified earlier, it sends an error message explaining why
the commit doesn't meet our commit style standards, and it exits the script
with an exit code of `1`. Recall, this means the commit push will be rejected.
Why do the `echo` statements start with `GL-HOOK-ERR`? This script was written
for a `GitLab` server, and
[gitlab specifies](https://docs.gitlab.com/ee/administration/server_hooks.html#custom-error-messages){: target="_blank", rel="noopener noreferrer" }
it will display error messages sent
to `stdout` in its user interface only if they begin with `GL-HOOK-ERR`.

Here's a pic of the GitLab user interface showing this error when a commit
fails this style guide function.

PIC OF STYLE ERROR MESSAGE

```bash
# Check that lines do not exceed character limit
function check_msg_line_lengths
{
    msg="$1"
    IFS=$'\n' lines=("$msg")
    for line in ${lines}
    do
        string_length=${#line}
        if [[ $string_length -gt $MAX_LINE_LENGTH  ]]
        then
            echo "GL-HOOK-ERR: Commit message contains one or more lines longer than ${MAX_LINE_LENGTH} characters."
            echo "GL-HOOK-ERR: First line that exceeds character limit:"
            echo "GL-HOOK-ERR: ${line}"
            exit 2
        fi
    done
}
```

↑ This bash function also receives the commit message as an argument.
It splits the commit message on by line on the newline symbol (`\n`).
It then loops over those lines. If a line is longer than our `MAX_LINE_LENGTH`
that we set earlier, it sends an error message specifying the first
line that was too long, and then it exits the script, preventing the commit
push from succeeding.

Here's a pic of the GitLab user interface showing this error when a commit
fails this line length function.

PIC OF LINE LENGTH ERROR MESSAGE

```bash
while read line
do
    # Only if line is not empty.
    if [[ -n "${line// }" ]]; then
        # Split the line into array.
        IFS=' ' read -r -a array <<< "$line"
        # This is the standard Git behavior for pre-receive:
        parent_sha=${array[0]}
        current_sha=${array[1]}
        ref=${array[2]}
        # Exit with success if push is not to `main` branch
        if [[ "$ref" != "$MAIN_BRANCH" ]]; then
            exit 0
        fi
        # Should only be one item in rev-list if this is a squash commit
        for commit in $(git rev-list "${parent_sha}".."${current_sha}"); do
            commit_msg="$(git cat-file commit "${commit}" | sed '1,/^$/d')"
            check_msg_style "$commit_msg"
            check_msg_line_lengths "$commit_msg"
        done
    fi
done < "${ST:-/dev/stdin}"
```

↑ This bit of code reads the input that `git` sends to the `pre-receive` hook
when that hook executes. Note that the input isn't sent as arguments to the
pre-receive script, but instead as a one line input stream.

That input stream looks something like this:

```bash
f167a945c1f784704e4b70cedc2c2b5a84fc0164 c1cddaaef0f66730da8e85ce5f8900fe836794bb refs/heads/some_branch
```

`while read line` is a while loop that loops over every line of input received
(there should only be one line, but just in case `if [[ -n "${line// }" ]]; then`
ignores blank lines if there are any). `IFS=' ' read -r -a array <<< "$line"`
splits the input stream line into an array with three items. The first
array item is the `parent_sha` a hash representing the last commit before new
commits were added to this branch. The second array item is the `current_sha`,
a hash representing the most recent commit to this branch. The third and final
array item is the `ref` that represents the branch being pushed to.

```bash
if [[ "$ref" != "$MAIN_BRANCH" ]]; then
    exit 0
fi
```

↑ This snippet checks that the ref is referring to the `main` branch. We
only care that commit messages pushed to the `main` branch follow our commit
message style rules, so ignore other branches by exiting immediately with
`0` exit status (success).

```bash
for commit in $(git rev-list "${parent_sha}".."${current_sha}"); do
    commit_msg="$(git cat-file commit "${commit}" | sed '1,/^$/d')"
    check_msg_style "$commit_msg"
    check_msg_line_lengths "$commit_msg"
done
```

↑ This section of code loops over every commit added in this push. It extracts
the commit message for each of those commits. It then passes that commit message
into our two style checking functions we defined earlier (exiting and failing
the script immediately if the commit message style standard is not met).
We have a git policy that pushes to the `main` branch are squashed into a
single commit, so the loop only looks at a single squash commit message. If
you didn't squash the commits, each commit message would have to match the
style rules. Git commits can be squashed automatically with settings in
GitLab or GitHub.

```bash
exit 0
```

↑ Finally, if the script didn't fail elsewhere, we exit with code `0` (success).
In this case, the pushed commit(s) will be accepted.

## How to test and install a pre-receive hook in GitLab


