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
