justify
=======

# About

Program to build left AND right justified output for a given string.


# Requirements

* Python >=3.7.5
* For testing, it's required to have `pytest` >=5.3.5 (can be installed as `pip3 install pytest==5.3.5`)


# Running

`jusitfy.py <width> <'file'|'stdin'> <path to file|text>`

## Positional Parameters

* `<width>` – expected width of the paragraph, non-negative integers
* `<'file'|'stdin'>` – "file" or "stdin" to denote incoming string source
* `<path to file|text>` – path to file to read from or directory the text, see examples

## Outputs

* to stdin - resulting string
* to stderr – all the debug messages and/or error messages

## Return codes

* 0 – successs
* 1 - insufficient arguments
* 2 – invalid width
* 3 – invalid input source
* 4 – non-existent path if source if `file`
* 5 – empty input, yet will produce empty line in stdout
* 6 – unjustifiable string for the given width

# Examples

```
➜ cat file
This is a sample text but a complicated problem to be solved, so we are adding more text to see that it actually works.
➜ ./justify.py 20 file file 2>/dev/null
This  is  a   sample
text      but      a
complicated  problem
to be solved, so  we
are adding more text
to   see   that   it
actually      works.
```

```
➜ ./justify.py 20 stdin "$(cat << _EOF
        hello
my string contains tabs
_EOF
)" 2>/dev/null
hello   my    string
contains        tabs
```

Example with debug output
```
➜ ./justify.py 7 stdin "hi it is vlad"
Init done.
Width: 7
From file: False
From: stdin
Contents:
hi it is vlad
wc = 2, wlen = 5, spaces = 1, available = 3, ratio = 3.0
wc = 2, wlen = 7, spaces = 1, available = 1, ratio = 1.0
hi   it
is vlad
```

# Testing

*Note: pytest must be installed*

As tests check positional parameters and returncodes, it is required to pass `--capture=sys`

`pytest -vv --capture=sys test_task.py`

