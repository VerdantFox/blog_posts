# VIM beginners guide and cheat sheet

tags: vim, settings, editors

## Introduction

VIM IMAGE

The command line text editor `vim` is *popular* in the world of programming,
and for good reason. It can be found on nearly any unix (and often Windows)
system, making it ideal for loading into a remote machine and making edits
to files. It is also very powerful in the right hands. If you watch someone
who knows what they're doing code with `vim`, the cursor is bouncing all over
as they quickly write and edit their files super fast, all without
ever touching a mouse....

I am *not* one of those people. I picked up `vim` out of necessity while
working on remote hosts without access to a GUI text editor. But I wanted to
get a little better, so I took a
[vim Udemy course](https://www.udemy.com/course/vim-commands-cheat-sheet/)
and I've been using what I've learned to get a litte more efficent in `vim`.
If you're a `vim` beginner, this post will teach you the commands I found
most useful while learning / working in `vim`. And if your a casual `vim` user
like me, this post can serve as a cheat sheet for all the `vim` commands you
and I will continue to forget.

## The essentials

These are the set of commands that you *need* in order to enter a file,
make changes, and get out (with or without saving).

1. **Enter into a file for editing.**
   Type: `vim some_file.txt` or `vi some_file.txt`

2. **Exit a file without saving.** First press `Esc` to enter `Normal Mode`.
   Then type `:q!` + `ENTER`. `!` here basically means *force*, and vim
   won't exit without it if you've made any changes.

3. **Save a file and exit.** First press `Esc` to enter `Normal Mode`.
   Then type `:wq` + `ENTER`. Bonus: `w` + `ENTER` without `q`,
   will save the file *without* exiting.

4. **Enter `Insert Mode`.** This is the mode where you can add text to the file.
   While in `Normal Mode`, press `i`. Recall you can press `Esc` whenever you
   want to exit `Insert Mode` to go back to `Normal Mode`.

## Navigation

These commands will get you around the file with ease. Notice where I use
`capital` vs `lower case` letters, as I might not always point it out.
Case matters in `vim`. For all of the following commands in this section,
unless otherwise specified, I'll assume you are in `Normal Mode`
(recall get here by hitting `Esc`).

1. **Move up, down, left, and right.** There are two main ways to move in
   these directions. You can use the `up`, `down`, `left`, `right` arrow
   keys in *any* mode. If you are in `Insert Mode`, these are the only keys
   for navigating.

   However, from `Normal Mode`, you can navigate in these directions
   without leaving typing position:

   `h` is`left`, `j` is `up`, `k` is down, and `l` is right. Notice the
   left most key of these keys is `left`, the right most is `right`, and
   the middle to are `up` followed by `down`.

2. **Go to start of file.** Press `g` + `g`.

3. **Go to end of file.** Press capital (`shitft`) `G`.

4. **Go to a specific line in file.** Type `:` + **line number** + `ENTER`
   to go to that line number. Eg. `:` + `25` + `ENTER` to go to line 25.

5. **Go to start of line.** Type `0` (zero). You can also press `^` (carrot)
   (ie `SHIFT`, `6`) to go to first *non-blank* character of a line.
   You might recall `^` is the start character for `regex`expressions.

6. **Go to end of line.**  Type `$` (dollar sign)(ie`SHIFT`, `4`).
   You might recall `$` is the end character for `regex` expressions.

7. **Move forward one word.**  Type `w`. I find this
   to be a quick way of moving through a line.

8. **Search for a word.**  type `/` + **search** + `ENTER`.
   E.g. `/foo` + `ENTER` will search for all instances of "foo" in the text.
   Note if `hlsearch` setting is set, found searches will start highlighting
   as you type. To go to next found search hit `n`, or to to previous found
   search hit capital `N`. You can remove the previous search's highlight by
   typing `:noh` (for no highlight), or if you can't remember this (and I just
   looked `:noh` up so obviously I can't), just search for something new that
   doesn't exist. Eg. `/asdfasdfas` + `ENTER`.

## Entering `Insert Mode` with style

There are a host of ways to enter `Insert Mode` in order to start writing
new text at different places. Here are the most useful ones. For all these
commands I will assume you are already in `Normal mode` (`Esc`).

1. **Enter `Insert Mode` in place.** Press `i`. I already mentioned this one
   in section one. This will enter `Insert Mode` one character *before* the
   character your cursor is on.

2. **Enter `Insert Mode` at line beginng.** Press capital `I` to enter 
   `Insert Mode` at the *beginning* of the line containing your cursor.

3. **Enter `Insert Mode` with append.** Press `a` to enter `Insert Mode` one
   character *after* the character your cursor is on.

4. **Enter `Insert Mode` at line end.** Press capital `A`
   to enter `Insert Mode` at the *end* of the line containing your cursor.

5. **Enter `Insert Mode` below your current line.** Press `o` to create
   a new line *below* the line containing your cursor and enter `Insert Mode`
   there. Note this will *not* break the line in half if your cursor is mid line.

6. **Enter `Insert Mode` above your current line.** Press capital `O` to
   create a new line *above* the line containing your cursor and enter
   `Insert Mode` there.

## Undo, Redo, Copy, Paste

## Deleting things

## Replace mode

## Doing things in multiples

## Macros?

## Vim settings
