# How to git rebase main/master onto feature branch

tags: git

## Introduction

GIT IMAGE

Does your project prefer `git rebase` instead of `git merge`? Has your branch
fallen out of sync with the `main` branch and you are unable to automate
your rebase due to conflicts? If so you might have run into rebase hell.
This happens when you try to rebase, solve your conflicts, and push to the
`main` branch, only to find that the `main` branch says you are now out of
sync once again in a never ending loop. Lets break out of rebase hell with
this short guide to rebasing.
