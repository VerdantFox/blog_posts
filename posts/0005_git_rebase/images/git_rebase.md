# How to git rebase main/master onto your feature branch even with merge conflicts

tags: git

## Introduction

REBASE IMAGE

Does your project prefer `git rebase` instead of `git merge`? Has your branch
fallen out of sync with the `main` branch and you are unable to automate
your rebase due to conflicts? If so, you might have run into rebase hell.
This happens when you try to `git rebase`, solve your conflicts, and push to the
`main` branch, only to find that the `main` branch is now, once again, out of
sync in a never-ending loop. Let's break out of rebase hell with
this short guide to rebasing.

## The steps

1. Go to the branch in need of rebasing
2. Enter `git fetch origin` (This syncs your main branch with the latest changes)
3. Enter `git rebase origin/main` (or `git rebase origin/master` if your main branch is named `master`)
4. Fix merge conflicts that arise however you see fit
5. After fixing merge conflicts, `git add FILE` previously merge conflicted files
6. Enter `git rebase --continue` (or `git rebase --skip` if `git` complains that there were no changes after resolving all conflicts)
7. Repeat as necessary as merge conflicts arise in the subsequent commits
8. Once the rebase is complete, enter `git push origin HEAD --force`

    This command pushes your rebase fixed branch to `remote`. The `--force` is important
    as it tells remote, "I know these changes are correct, accept them as is."
    Without the `--force` flag, your remote branch will continue to believe
    it is out of sync and will claim a merge conflict.

And that's it. You have now `git rebase`d the `main` branch onto your
feature branch and broken yourself out of rebase hell.
