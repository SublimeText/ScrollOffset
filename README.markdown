ScrollOffset
============
ScrollOffset automatically scrolls the buffer when the insertion point gets near the edge, similar to how vim's scrolloff works. ScrollOffset works with multiple selections, and you can change how far from the edge you'd like to stay.

This Plugin is implemented using Layout-Coordinates, so it also works when you have `word_wrap` enabled.

When you use multiple selections which do not fit into the viewport, Sublimes default behviour is used. This might change in future versions - you find a `TODO` in the code where to add the logic for such behaviour.


Ignoring Mouse Input
--------------------
ScrollOffset runs whenever the selection changes. If you would like to ignore mouse input for ScrollOffset purposes, you must also install [MouseEventListener](https://github.com/SublimeText/MouseEventListener). Once MouseEventListener is installed, ScrollOffset will automatically start ignoring mouse input.

However, selecting more than the viewport can display still feels a bit awkward. Since Sublime does not offer a possibility to detect
mouse dragging, one can not implement Sublimes default behaviour when it comes to those kind of selections. Just try it out whether it's
a hassle for you.


Install
-------

This plugin is available through Package Control, which is available here:

    http://wbond.net/sublime_packages/package_control

As mentioned above, installing [MouseEventListener](https://github.com/SublimeText/MouseEventListener) is good idea.


Manual Install
--------------

Go to your Packages subdirectory under ST2's data directory:

* Windows: %APPDATA%\Sublime Text 2
* OS X: ~/Library/Application Support/Sublime Text 2
* Linux: ~/.config/sublime-text-2
* Portable Installation: Sublime Text 2/Data

Then clone this repository:

    git clone git://github.com/Wolff09/ScrollOffset.git

That's it!
