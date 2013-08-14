Two days ago, looking for a possible [Eclipse][] replacement, I gave a try to [Sublime Text 2][].
One of my main usages of [PyDev][] (very good Eclipse plug-in for Python developer) is the code formatter.
Under ST2 I installed [PythonTidy][] but unfortunately it did not work for me.
So, for fun and learning, I decided to create a new ST2/ST3 plug-in: **Python PEP8 Autoformat**.
It is based on [autopep8][] as code formatter and [pep8][] as code linter.

# Python PEP8 Autoformat

Python PEP8 Autoformat is a Sublime Text 2/3 plug-in to interactively reformat Python source code according to [PEP-8][] (Style Guide for Python Code). 

## Installation

To avoid dependencies, all necessary modules are included within the package.

### Sublime Text 3

Since Sublime Text 3 no longer extracts the contents of .sublime-package files by default, and the fact that Python PEP8 Autoformat needs to read files from disk, the only viable install method right now is manual.

1. Using mercurial (hg) repository on bitbucket:
    + Open a terminal, move to Packages directory (refers to the folder that opens when you use the Preferences > Browse Packages… menu). Then type in terminal:
    + `hg clone https://bitbucket.org/StephaneBunel/pythonpep8autoformat 'Python PEP8 Autoformat'`

1. Manually:
    + Download an [archive][TagArchive]
      of Python PEP8 Autoformat.
    + Open a terminal, move to Packages directory (refers to the folder that opens when you use the Preferences > Browse Packages… menu) and create a new directory named 'Python PEP8 Autoformat'
    + Extract archive contents in this 'Python PEP8 Autoformat' directory.

### Sublime Text 2

1. Using [Sublime Package Control][]
    + Use `cmd+shift+P` shortcut then `Package Control: Install Package`
    + Look for `Python PEP8 Autoformat` and install it.

1. Using mercurial (hg) repository on bitbucket:
    + Open a terminal, move to Packages directory (refers to the folder that opens when you use the Preferences > Browse Packages… menu). Then type in terminal:
    + `hg clone https://bitbucket.org/StephaneBunel/pythonpep8autoformat 'Python PEP8 Autoformat'`

1. Manually:
    + Download an [archive][TagArchive]
      of Python PEP8 Autoformat
    + Open a terminal, move to Packages directory (refers to the folder that opens when you use the Preferences > Browse Packages… menu) and create a new directory named 'Python PEP8 Autoformat'
    + Extract archive contents in this 'Python PEP8 Autoformat' directory.

## Settings

You'll find settings in Preferences menu (Preferences -> Package Settings -> Python PEP8 Autoformat -> ...).

    {
        // autoformat code on save ?
        "autoformat_on_save": false,

        // enable possibly unsafe changes (E226, E24, W6)
        // aggressive level, 0 to disable:
        "aggressive": 0,

        // list codes for fixes; used by --ignore and --select
        "list-fixes": false,

        // do not fix these errors / warnings (e.g. ["E501", E4", "W"])
        "ignore": [],

        // select errors / warnings (e.g. ["E4", "W"])
        "select": [],

        // Maximum line length
        "max-line-length": 79
    }

By editing User settings, your personal liking will be kept safe over plug-in upgrades.

## Usage

Formatting is applied on the whole document.

### Using keyboard:

- GNU/Linux: `ctrl+shift+r`
- OSX:       `ctrl+shift+r`
- Windows:   `ctrl+shift+r`

### Using Command Palette:

As defined in `Default.sublime-commands` file:

	[
	    { "caption": "User: Python PEP8 Autoformat", "command": "pep8_autoformat" }
	]

You can format your Python code by opening Command Palette (ctrl+shift+P)
and type "auto"... up to highlight full caption.

### Companions
Useful companions to Python PEP8 Autoformat:

+ [SublimeLinter][] - Inline lint highlighting
+ [MarkdownPreview][] - Markdown preview in browser

## License

Copyright 2012-2013 Stéphane Bunel

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


[PEP-8]:                   http://www.python.org/dev/peps/pep-0008/
[Sublime Text 2]:          http://www.sublimetext.com/
[autopep8]:                https://github.com/hhatto/autopep8
[pep8]:                    https://github.com/jcrocholl/pep8
[PythonTidy]:              https://github.com/witsch/SublimePythonTidy
[Eclipse]:                 http://www.eclipse.org/
[PyDev]:                   http://pydev.org/
[Sublime Package Control]: http://wbond.net/sublime_packages/package_control
[SublimeLinter]:           https://github.com/SublimeLinter/SublimeLinter
[MarkdownPreview]:         https://github.com/revolunet/sublimetext-markdown-preview
[TagArchive]:              https://bitbucket.org/StephaneBunel/pythonpep8autoformat/downloads/#tag-downloads