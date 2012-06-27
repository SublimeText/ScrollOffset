ScrollOffset
============
ScrollOffset automatically scrolls the buffer when the insertion point gets near the edge, similar to how vim's scrolloff works. ScrollOffset works with multiple selections, and you can change how far from the edge you'd like to stay.

Ignoring Mouse Input
--------------------
ScrollOffset runs whenever the selection changes. If you would like to ignore mouse input for ScrollOffset purposes, you must also install [MouseEventListener](https://github.com/SublimeText/MouseEventListener). Once MouseEventListener is installed, ScrollOffset will automatically start ignoring mouse input.

Install
-------

This plugin is available through Package Control, which is available here:

    http://wbond.net/sublime_packages/package_control

Manual Install
--------------

Go to your Packages subdirectory under ST2's data directory:

* Windows: %APPDATA%\Sublime Text 2
* OS X: ~/Library/Application Support/Sublime Text 2
* Linux: ~/.config/sublime-text-2
* Portable Installation: Sublime Text 2/Data

Then clone this repository:

    git clone git://github.com/SublimeText/ScrollOffset.git

That's it!

