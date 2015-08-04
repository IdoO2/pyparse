# pyparse

## What’s in it

Creates view with tree virtually representing code.

Files:

- `view.py` handles the Qt application & tree view
- `qmodel.py` is the model
- `parsermoc.py` basically implements the public interface of the parser

## How to run

Once cloned, `python view.py` from a terminal shall open a window with an
example tree. See documentation in files.

## Requirements

Should work with any variants of Python 3 and  PyQt 5.

## Changelog

### Update 2015-08-04

Intermediary state of standalone application: user interface class acts as
controller leveraging model, view and parser to achieve functionality.

### Update 2015-08-02

Another, more radical cleanup, after project shifted from ST plugin to
standalone application.  Relevant files are still in the `src` folder. Concerns
need better separation, but roughly `main.py` is the entry point and
orchestrates application setup; `parsermoc.py` is a placeholder parser;
`qmodel.py` is the model; `view.py` should handle the user interface but is
getting something of a controller’s responsibility.

The application can be run using the `run` executable at root.

### Update 2015-07-15

Reasonable cleanup of repository. Relevant code has been moved to `src` folder.
Functionally no difference with previous version.


### Update 2015-07-14

We are now able to basically run a plugin. Relevant files are `stplugin.py`,
`parsemoc.py` and `build.sh`. Running build.sh will move the two other files to
the ST plugin directory and run Sublime Text. The moc plugin should work: when a
file gains focus, a parser is initialised; on save, the parser receives the
update.
