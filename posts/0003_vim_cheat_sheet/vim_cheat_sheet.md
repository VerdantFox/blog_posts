# VIM beginners guide and cheat sheet

tags: vim, editors, settings

## Introduction

VIM IMAGE

The command line text editor `vim` is *popular* in the world of programming,
and for good reason. It can be found on nearly any unix (and often Windows)
system, making it ideal for loading into remote machines and making quick edits
to files. It is also very powerful in the right hands. If you watch an
expert `vim` user code with `vim`, the cursor is bouncing all over
as they quickly write or edit their files, all without ever touching a mouse....

I am *not* one of those people. I picked up `vim` out of necessity while
working on remote hosts without access to a GUI text editor (I'm partial
to VS Code). But since I needed to use `vim`, I wanted to get better at it, so I
took a [vim Udemy course](https://www.udemy.com/course/vim-commands-cheat-sheet/),
and I've been using what I've learned to get a little more efficent in `vim`.
If you're a `vim` beginner, this post will teach you the commands I found
most useful while learning `vim`. And if you're a casual `vim` user
like me, this post can serve as a cheat sheet reminder for all the `vim`
commands you and I will continue to forget.

## The essentials

These are the set of commands that you *need* in order to enter a file,
make changes, and get out (with or without saving).

1. **Enter into a file for editing:**
   Type: `vim some_file.txt` or `vi some_file.txt` to enter a file with `vim`.

2. **Exit a file without saving:** First press `ESC` to enter `Normal Mode`.
   Then type `:q!` + `ENTER`. `q` here means "quite" while `!` basically means
   *force*, and `vim` won't exit without it if you've made any changes.

3. **Save a file and exit:** First press `ESC` to enter `Normal Mode`.
   Then type `:wq` + `ENTER`. `w` means "write" here so you can also just
   use `:w` + `ENTER` without `q` to save the file *without* exiting.

4. **Enter `Insert Mode`:** This is the mode where you can add text to the file.
   While in `Normal Mode`, press `i` (for "insert"). Recall that you can press
   `ESC` whenever you want to exit `Insert Mode` in order to go back to `Normal Mode`.

## Navigation

These commands will get you around the file with ease. Notice where I use
`capital` vs `lowercase` letters, as I might not always point it out.
Case matters in `vim`. For all of the following commands in this section,
unless otherwise specified, I'll assume you are in `Normal Mode`
(recall you can get there by hitting `ESC`).

1. **Move up, down, left, and right:** There are two main ways to move in
   these directions. You can use the `up`, `down`, `left`, and `right` arrow
   keys in *any* mode. If you are in `Insert Mode`, these are the *only* keys
   for navigating. However, from `Normal Mode`, you can navigate in these
   directions without leaving typing position: `h` is`left`, `j` is`up`,
   `k` is `down`, and `l` is `right`. Notice the left-most key of these 4
   keys (`h`) is `left`, the right-most key (`l`) is `right`, and the
   middle two are (`j`) `up` followed by (`k`) `down`.

2. **Go to the start of the file:** Press `g` + `g` to go to the start of the file.

3. **Go to end of the file:** Press capital `G` (ie `SHIFT-G`) to go to the
   end of the file.

4. **Go to a specific line in the file:** Type `:LIN_NUM` + `ENTER`
   to go to that line number. Eg. `:25` + `ENTER` to go to line 25.

5. **Go to the start of the current line:** Type `0` (zero) to go to the
   start of the current line. You can
   also press `^` (carrot)(ie `SHIFT-6`) to go to the first *non-blank*
   character of the line. You might recall that `^` is the **start** character
   for `regex`expressions.

6. **Go to the end of the current line:**  Type `$` (dollar sign)(ie`SHIFT-4`)
   to go to the end of the current line.
   You might recall `$` is the **end** character for `regex` expressions.

7. **Move forward one word:**  Type `w` to move your cursor to the next word.
   I find this to be a quick way of moving through a line.

8. **Search for a word:**  type `/` + **SEARCH** + `ENTER` to search for a word.
   E.g. `/foo` + `ENTER` will search for all instances of "foo" in the text.
   Note if `hlsearch` setting is set, found searches will start highlighting
   as you type. To go to the next found search item, press `n`, or to to previous found
   search item, press capital `N`. You can remove the previous search's highlight by
   typing `:noh` (for no highlight), or if you can't remember this (and I just
   looked `:noh` up so obviously I can't), just search for something new that
   doesn't exist. Eg. `/asdfasdfas` + `ENTER`.

## Entering `Insert Mode` with style

There are a host of ways to enter `Insert Mode` in order to start writing
new text. Here are the most useful ones. For all these
commands, I will assume you are already in `Normal mode` (`ESC`).

1. **Enter `Insert Mode` in place:** Press `i` to enter `Insert Mode` one
   character *before* the character your cursor is on. I already mentioned
   this one in section one.

2. **Enter `Insert Mode` at line beginng:** Press capital `I` to enter
   `Insert Mode` at the *beginning* of the line containing your cursor.

3. **Enter `Insert Mode` with append:** Press `a` to enter `Insert Mode` one
   character *after* the character your cursor is on.

4. **Enter `Insert Mode` at line end:** Press capital `A`
   to enter `Insert Mode` at the *end* of the line containing your cursor.

5. **Enter `Insert Mode` below your current line:** Press `o` to create
   a new line *below* the line containing your cursor and enter `Insert Mode`
   there. Note this will *not* break the line in half if your cursor is mid line.

6. **Enter `Insert Mode` above your current line:** Press capital `O` to
   create a new line *above* the line containing your cursor and enter
   `Insert Mode` there.

## Undo, Redo

Sometimes you make a mistake and really need to un-make that mistake.
You could `:q!` to exit without saving, but lets see if we can find a
less drastic solution. These commands should be performed from
`Normal Mode` (`ESC`).

1. **Undo:** Press `u` to undo. Uppercase `U` undoes all latest changes on
   one line (which I don't really use).

2. **Redo:** Press `Ctrl-r` to redo.

## Deleting things (and cut)

There are multiple ways to delete different sized chunks of code in vim.
Lets take a look at some of the more common ones. `d` stands for delete in `vim` so
commands focus around this key. Note that `vim` *always* saves the last deleted
thing to the default `register` (more on `registers` later). So in a sense,
there is no `delete`, just `cut` with short term memory. All these commands
should be performed from `Normal Mode` (`ESC`).

1. **Delete/cut a letter:** Press `d` + `l` to delete a letter and save it to
   the default `register`.

2. **Delete/cut a word:** Press `d` + `w` to delete a word and save it to the
   default `register`.

3. **Delete/cut a line:** Press `d` + `d` to delete a line and save it to the
   default `register`.

Also note that while in `Insert Mode` you can use `BACKSPACE` and `DEL` as usual
to delete characters *before* or *after* your cursor respectivly. This form
of deletion does not save to the default `register`.

## Copy/paste

We've already seen how to `cut` (the same as deleting). Here we see
how to `copy` items to the register and also to `paste` items from the register.
Copying in `vim` is called `yank`ing, so those commands use `y`.
All these commands should be performed from `Normal Mode` (`ESC`).

1. **Copy/yank a letter:** Press `y` + `l` to copy a letter to the default `register`.

2. **Copy/yank a word:** Press `y` + `w` to copy a word to the default `register`.

3. **Copy/yank a line:** Press `y` + `y` to copy a line to the default `register`.

4. **Paste after the cursor:** Press `p` to paste whatever is in the default `register`
   immediately *after* the character the cursor is hovering over.

5. **Paste before the cursor:** Press capital `P` to paste whatever is in the
   default `register` immediately *before* the character the cursor is hovering over.

What is this `register` I keep mentioning? Briefly, a `register` can store
copied/cut text. A register can be "named". For example, to copy to the `b`
*named* `register` you could type `"b` followed by your `yank`. And then to
use that `yank`ed text, type `"b` + `p`. The *default* `register` is where
text is stored and pasted from if you don't use a named register.
Only the *latest* copy/cut text is stored in a `register`. Subsequent
stores override the previous store. If `registers` interests you,
give them a quick google search for more details.

Also note these commands are only for copy/paste from *within* vim. Copying and pasting
from the system clipboard is trickier. While it is possible with key
commands, usually I've had success just using good old fashion mouse
`right click` + `click dropdown item` for this purpose, so just do that.

## `Replace Mode`

`Replace Mode` is like `Insert Mode`, except all typed characters overwrite
whatever the cursor is hovering. These commands should begin in `Normal Mode`
(`ESC`).

1. **Replace a single character:** Place cursor over the character to be replaced
   and press `r` + **NEW CHARACTER** (ie `r` + `f`) to replace the hovered
   character with "f". Vim will immediately re-enter `Normal Mode` after
   replacing this character.

2. **Replace multiple characters:** Place cursor over the character you want
   to start replacing at and press capital `R`. Vim will enter `Replace Mode`
   at that character and all subsequent characters typed will replace
   the following characters on that line. For instance with cursor over the
   the "d" from "dog", I could type `Rcat` to replace "dog" with "cat". To
   exit replace mode you can hit `ESC`.

## Doing things in multiples

Vim has a cool sentence structure like syntax that you can use to perform
actions. We saw this earlier with commands like `d` + `w` for "delete a word".
Adding a number at the start of these sentence like commands will perform that
command that number of times. For instance to "delete 3 words" I could type
`3` + `d` + `w` and the hovered word plus the next two will be deleted.
To copy (yank) 2 lines, I can type `2` + `y` + `y`. And to undo the last 4
actions I could type `4` + `u`. Neat, eh?

## Bonus: Vim settings

I think `vim` is much nicer when it is configured the way you like it. Here's
a list of settings *I* like to use when running vim. Put these settings
(plus or minus the ones *you* like) into a file at `~/.vimrc`. In the file,
`"` at the start of a line means it is a comment.

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

These were the `vim` commands (and settings) I found most useful in breaking
past the bare minimum of what it takes to code in `vim`.
As I said earlier, I am by no means a `vim` expert. I've only recently been
using `vim` commands more complicated than the ones I listed in "vim essentials".
But now that I've learned some of these neat commands, I have to say,
vim is not so scary anymore and is actually pretty pleasant to code in.

Vim is very powerful and there is a *lot* you can do with it. I'm sure vim
experts would disagree with some of my  choices for a curated list of commands.
A couple other `vim` topics I left out that you should look into if you want
to get "good" with `vim` are:

- Using the `vim` manual to look all these commands and ideas up yourself
- Macros (save a series of `vim` commands to 1 or 2 keystrokes)
- `vim` replace (replace words/phrases found with `vim` search)
- `Visual Mode` (make more complex edits in grid like patterns)
- Many others I can't think of right now

If you are interested in a `vim` deep dive, I highly recommend the
[Vim masterclass Udemy course](https://www.udemy.com/course/vim-commands-cheat-sheet/)
where you can learn these commands and many others and how to
"think like a `vim` user" to really speed up your `vim` coding.
