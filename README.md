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

## Changelog

### Update 2015-07-14

We are now able to basically run a plugin. Relevant files are `stplugin.py`,
`parsemoc.py` and `build.sh`. Running build.sh will move the two other files to
the ST plugin directory and run Sublime Text. The moc plugin should work: when a
file gains focus, a parser is initialised; on save, the parser receives the
update.
