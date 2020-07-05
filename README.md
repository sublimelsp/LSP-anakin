# LSP-anakin

This is a helper package that automatically installs and updates the
[Anakin Language Server](https://github.com/muffinmad/anakin-language-server) for you.

To use this package, you must have the [LSP](https://packagecontrol.io/packages/LSP) package installed as well.

## Applicable Selectors

This language server operates on views with the `source.python` base scope.

## Installation Location

The server is installed in the $DATA/Cache/LSP-anakin directory, where $DATA is the base data path of Sublime Text.
For instance, $DATA is `~/.config/sublime-text` on a Linux system. If you want to force a re-installation of the server,
you can delete the entire $DATA/Cache/LSP-anakin directory. The installation is done through a virtual environment,
using pip. Therefore, you must have at least the `python` executable installed and it must be present in your $PATH.

Like any helper package, installation starts when you open a view that is suitable for this language server. In this
case, that means that when you open a view with the `source.python` base scope, installation commences.

## Configuration

Configure the Python Language Server by accessing `Preferences > Package Settings > LSP > Servers > LSP-anakin`.

## Code Completion

This language server provides code completion through JEDI.

## Signature Help

This language server provides signature help through JEDI.

## Goto

This language server provides "goto definition" through JEDI.

## Find References

This language server provides "find references" through JEDI.

## Rename

This language server provides "rename word/symbol" through JEDI.

## Code Actions

This language server can inline variables for you with a code action.

## Linters

The default linters used are `pycodestyle` and `pyflakes`. You can optionally enable `mypy`.
*This language server starts linting after you save a view.*

## Formatters

The formatter is `yapf`.

## Sublime Text Plugin Development

By default, the environment of pyls is adjusted so that the `PYTHONPATH` includes the directory where `sublime.py` and
`sublime_plugin.py` live, as well as the $DATA/Packages directory. This enables accurate code completion for these
files.
