SublimeEvernote
===============

[Sublime Text 2](http://www.sublimetext.com/2) plugin for [Evernote](http://www.evernote.com) 


### Install

Through [Package Control](http://wbond.net/sublime_packages/package_control)

`Command Palette` > `Package Control: add Repository` && `input 'http://github.com/oparrish/SublimeEvernote`

`Command Palette` > `Package Control: Install Package` > `SublimeEvernote`

or clone this repository in

* Windows: `%APPDATA%/Roaming/Sublime Text 2/Packages/`
* OSX: `~/Library/Application Support/Sublime Text 2/Packages/`
* Linux: `~/.Sublime Text 2/Packages/`
* Portable Installation: `Sublime Text 2/Data/`

### Usage

`Command Palette` > `Send to evernote`

`Context menu` > `Send to Evernote`

`Context menu` > `Evernote settings`

#### Markdown Support ####

Write notes in Markdown and they will be processed when they are sent to Evernote.

This:
![this](https://dl.dropbox.com/u/643062/SublimeEvernoteScreenshots/Markdown.png)

Turns into this:
![this](https://dl.dropbox.com/u/643062/SublimeEvernoteScreenshots/Evernote.png)

#### Metadata ####

Use metadata block to specify title and tags.

    ---
    title: My Note
    tags: tag1,tag2
    ---


    http://127.0.0.1/?oauth_token=oparrish-4096.13CD316B8E2.687474703A2F2F3132372E302E302E31.FFDE4D1D8E8BEB44873A064E7DEAD2BC&oauth_verifier=4DFD95C896151EF579B00B94F69F17DC