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

3. **Go to end of file.** Press capital `G` (ie `SHIFT-G`).

4. **Go to a specific line in file.** Type `:` + **line number** + `ENTER`
   to go to that line number. Eg. `:` + `25` + `ENTER` to go to line 25.

5. **Go to start of line.** Type `0` (zero). You can also press `^` (carrot)
   (ie `SHIFT-6`) to go to first *non-blank* character of a line.
   You might recall `^` is the start character for `regex`expressions.

6. **Go to end of line.**  Type `$` (dollar sign)(ie`SHIFT-4`).
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


## Undo, Redo

Sometimes you make a mistake and really need to un-make that mistake.
You could `:q!` to exit without saving, but lets see if we can use
less drastic solutions. These commands should be performed from
`Normal Mode` (`Esc`).

1. **Undo.** Press `u`. Uppercase `U` undoes all latest changes on one line
   which I don't really use.

2. **Redo.** Press `Ctrl-R`.

## Deleting things (and cut)

There are multiple ways to delete different sized chunks of code in vim.
Lets take a look at some of the more common ones. `d` stands for delete in vim so
commands focus around this key. Note that vim *always* saves the last deleted
thing to the register. So in a sense, there is no `delete`, just `cut` with
short term memory. All these commands should be performed from `Normal Mode` (`Esc`).

1. **Delete/cut a letter.** Press `d` + `l`.

2. **Delete/cut a word.** Press `d` + `w`.

3. **Delete/cut a line.** Press `d` + `d`.

## Copy/paste

We've already seen how to `cut` above (the same as deleting). Here we see
how to `copy` items to the register and also to `paste` items from the register.
Copying in vim is called `yank`ing, so those commands use `y`.
All these commands should be performed from `Normal Mode` (`Esc`).

1. **Copy/yank a letter.** Press `y` + `l`.

2. **Copy/yank a word.** Press `y` + `w`.

3. **Copy/yank a line.** Press `y` + `d`.

4. **Paste after the cursor.** Press `p`.

5. **Paste beofre the cursor.** Press capital `P`.

Note that copy and paste is a little complicated in vim as you can copy
and paste to things called `registers` that store multiple copy/cuts under
character (mostly alphabetical) registers, but I'm not going to go into those
details. If that interests you, give it a quick google search. For our purposes
here only the *latest* copy/cut is stored in the *default* register.

Also note these are only for copy/paste from *within* vim. Copying and pasting
from the system clipboard is trickier. While it is possible with key
commands, usually I've had success just using good old fashioned mouse
`right click` + `click dropdown item` for this purpose, so just do that.

## `Replace Mode`

`Replace Mode` is like `Insert Mode`, except all typed characters overwrite
whatever the cursor is hovering. These commands should begin in `Normal Mode`
(`Esc`).

1. **Replace single character.** Place cursor over the character to be replaced
   and press `r` + **new character** (ie `r` + `f`) to replace the hovered
   character with "f". Vim will immediately re-enter `Normal Mode` after
   replacing this character.

2. **Replace multiple characters.** Place cursor over the character you want
   to start replacing at and press capital `R`. Vim will enter `Replace Mode`
   at that character and all subsequent characters typed will replace the
   the following characters. For instance with cursor over the the "d" from
   "dog", I could type `Rcat` to replace "dog" with "cat". To exit replace
   mode you can hit `Esc`.

## Doing things in multiples

Vim has a cool sentence structure like syntax that you can use to perform
actions. We saw this earlier with commands like `d` + `w` for "delete a word".
Add a number at the start of these sentence like commands will perform them
that number of times. For instance to "delete 3 words" I could type
`3` + `d` + `w` and the hovered word plus the next two will be deleted.
To copy (yank) 2 lines, I can type `2` + `y` + `y`. And to undo the last 4
actions I could type `4` + `u`. Neat, eh?

## Bonus: Vim settings

I think vim is much nicer when it is configured the way you like it. Here's
a list of vim settings I like to use when running vim. Put these settings
into a file `~/.vimrc`. In the file `"` at the start of a line means it is
a comment.

```vimrc
" use syntax highlighting
syntax on
" Show line number
set number
" Show the cursor position
set ruler
" Show incomplete commands
set showcmd
" Highlight searched words
set hlsearch
" Incremental search
set incsearch
" Search ignore case unless capitalized letters used in search
set ignorecase
set smartcase
" Don't line-break mid word
set lbr
" Set auto indent (auto indent when previous line was indented for coding)
set autoindent
" Set smart indent (smartly indent when code indicates indent should occur)
set smartindent
" Replace tab with spaces
set expandtab
" Set tab spacing to 4
set tabstop=4
set shiftwidth=4
set softtabstop=4
```

## Conclusions

These were the vim commands (and settings) I found most useful in breaking
past the bare minimum of what it takes to code in vim.
As I said earlier, I am by no means a vim expert. I've only recently been
using vim commands more complicated than the ones I listed in "vim essentials".
But now that I am, I have to say, it's not so scary anymore and is actually
pretty pleasant to code in.

Vim is very powerful and there is a *lot* you can do with it. I'm sure vim
experts would disagree with my curated list of commands. A couple other vim
topics I left out that you should look into if you want to get "good" with
vim are:

- Using the vim manual to look all these commands and ideas up yourself
- Macros (save a series of vim commands to 1 or 2 keystrokes)
- vim replace (replace words/phrases found with vim search)
- `Visual Mode` (make more complex edits in grid like patterns)
- Many others I can't think of right now

If you are interested in a vim deep dive, I highly recommend the
[Vim masterclass Udemy Course](https://www.udemy.com/course/vim-commands-cheat-sheet/)
where you will learn these commands and many others and how to
"think like a vim user" to really speed up your vim coding.
