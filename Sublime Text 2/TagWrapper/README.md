Sublime Text 2 plugin: TagWrapper
=================================

This plugin allows you to wrap selected text in given HTML tags or to strip
HTML tags from selection.

Using
-----

* Make one or more selections
* Press `alt+shift+t` to wrap the selection. You will be prompted to enter
  opening HTML tags (e.g., `<p class="paragraph"><strong>`). Closing tags will
  be inserted automatically.
* or press `alt+shift+s` to strip all HTML tags

Key bindings
-------------------

You may remap any of the default key bindings:

### Wrapping selection with prompt ###

	{ "keys": ["alt+shift+t"], "command": "tag_wrapper_input" }

### Stripping HTML tags from selection ###

	{ "keys": ["alt+shift+s"], "command": "strip_tags" }

### Wrapping selection without prompt ###

You may also add your own key bindings for predefined HTML tags. Example:

	{
		"keys": ["alt+shift+p"], "command": "tag_wrapper",
		"args": {
			"tag": "<p>"
		}
	}

Examples
--------

### Wrap contents of `<button />` in `<span />` tag (using Vintage) ###

	<button type="submit">Submit form</button>

Press `vit`, `alt+shift+t`, `<span class="x">`, `Enter`. Result:

    <button type="submit"><span class="x">Submit form</span></button>

### Wrap multiple rows in `<li>` tag (using Vintage) ###

	Lorem ipsum dolor sit amet
	consectetur adipisicing elit
	sed do eiusmod tempor incididunt
	ut labore et dolore magna aliqua

Press `alt+shift+down` until you select all rows, `v$`, `alt+shift+t`, `<li>`,
`Enter`. Result:

	<li>Lorem ipsum dolor sit amet</li>
	<li>consectetur adipisicing elit</li>
	<li>sed do eiusmod tempor incididunt</li>
	<li>ut labore et dolore magna aliqua</li>

Installation
------------

The recommmended method of installation is via **Package Control**.
It will download upgrades to your packages automatically.

### Package Control ###

* Follow instructions on [http://wbond.net/sublime_packages/package_control](http://wbond.net/sublime_packages/package_control)
* Install using Package Control: Install > TagWrapper package

### Using Git ###

Go to your Sublime Text 2 Packages directory and clone the repository
using the command below:

    git clone https://github.com/ignacysokolowski/SublimeTagWrapper "TagWrapper"

### Download Manually ###

* Download the files using the Github downloads option
* Unzip/untar the files and rename the folder to `TagWrapper`
* Copy the folder to your Sublime Text 2 Packages directory

Changelog
---------

### 1.0.0 ###

* Initial release
