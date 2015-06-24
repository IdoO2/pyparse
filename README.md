# pyparse

## What’s in it

Creates view with tree virtually representing code.

Files:

- `view.py` handles the Qt application & tree view
- `qmodel.py` is the model
- `parser.py` basically implements the public interface of the parser

## How to run

Once cloned, `python view.py` from a terminal shall open a window with an
example tree; a prompt in the terminal will allow updating the contents of the
tree. See documentation in files, `view` then `parser`.

## Requirements

Should work with any variants of Python 3 and  PyQt 5.
