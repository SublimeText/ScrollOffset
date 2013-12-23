"""
Known issue:
	- selecting near the edge of the screen with the mouse is kind of wonky
	- selecting more than the viewport can display with the mouse is kind of wonky
	- with word wrap activated, the courser might appear at very first position of a line
	  but sublime interpretes it as being at the very last position of the previous line
	  -> the specified margin might be larger/smaller by 1 line within wrapped lines
	- detecting mouse up would be nice (as far as I know, not possible with Sublime API)
"""

import sublime, sublime_plugin
try:
	import mouse_event_listener
except:
	pass


class ScrollOffset(sublime_plugin.EventListener):
	ignore_count = 0

	def on_pre_mouse_down(self, args):
		self.ignore_count = 3

	def on_post_mouse_down(self, click_point):
		self.ignore_count = 1

	def on_selection_modified(self, view):
		if self.ignore_count:
			self.ignore_count -= 1
			return
		if view.is_loading() or len(view.sel()) == 0:
			return
		
		########################################################################################
		################################ READ SETTINGS + HELPERS ###############################
		########################################################################################

		viewport_position = list(view.viewport_position()) # tupel to list, since mutable
		viewport_size = view.viewport_extent()
		line_height = view.line_height()
		em_width = view.em_width()

		settings = sublime.load_settings('Scroll Offset.sublime-settings')
		BOTTOM_OFFSET = settings.get("bottom_margin")
		TOP_OFFSET = settings.get("top_margin")
		VERTICAL_OFFSET = settings.get("vertical_margin")
		LEFT_OFFSET = settings.get("left_margin")
		RIGHT_OFFSET = settings.get("right_margin")
		HORIZONTAL_OFFSET = settings.get("horizontal_margin")

		TOP_DIST = int(TOP_OFFSET or VERTICAL_OFFSET or 0) * line_height
		BOTTOM_DIST = (int(BOTTOM_OFFSET or VERTICAL_OFFSET or 0) + 1) * line_height
		LEFT_DIST = int(LEFT_OFFSET or HORIZONTAL_OFFSET or 0) * em_width
		RIGHT_DIST = int(RIGHT_OFFSET or HORIZONTAL_OFFSET or 0) * em_width

		do_horizontal = LEFT_DIST > 0 or RIGHT_DIST > 0
		do_vertical = TOP_DIST > 0 or BOTTOM_DIST > 0

		def scroll_to(horizontal=None,vertical=None):
			viewport_position[0] = max(horizontal or viewport_position[0], 0)
			viewport_position[1] = vertical or viewport_position[1]
			vpos = viewport_position[0], viewport_position[1]
			view.set_viewport_position(vpos)


		########################################################################################
		####################################### VERTICAL #######################################
		########################################################################################

		def preserve_vertical_margin():
			# get the selection, default behaviour with multiple selections
			sel = view.sel()
			if len(sel) > 1:
				sel, multiple = sublime.Region(sel[0].begin(), sel[-1].end()), True
			else:
				sel, multiple = sel[0], False

			# get the top and bottom position of the selection
			top = view.text_to_layout(sel.begin())[1]
			bot = view.text_to_layout(sel.end())[1]

			# methods for scrolling to preserve vertical margin
			align_top = lambda: scroll_to(vertical=top - TOP_DIST)
			align_bot = lambda: scroll_to(vertical=bot + BOTTOM_DIST - viewport_size[1])

			# distance of selection to top/bottom of viewport
			dist_top = top - viewport_position[1]
			dist_bot = viewport_position[1] - bot + viewport_size[1]

			# preserve the vertical margin, maybe only at one side
			if viewport_size[1] - TOP_DIST - BOTTOM_DIST < bot - top:
				# we can only perserve the vertical margin at one side
				# decide which end of the selection is "active"
				if multiple:
					pass # TODO: imitate sublime behaviour
				else:
					# check for inverted selection
					if sel.a <= sel.b: align_bot()
					else: align_top()
			elif dist_top < TOP_DIST: align_top()
			elif dist_bot < BOTTOM_DIST: align_bot()


		if do_vertical:
			preserve_vertical_margin()
		

		########################################################################################
		###################################### HORIZONTAL ######################################
		########################################################################################

		def preserve_horizontal_margin():
			sel = view.sel()
			multiple = len(sel) > 1

			# get left and right position of selection
			def func(x, y):
				x1, x2 = x
				y1, y2 = view.text_to_layout(y.a)[0], view.text_to_layout(y.b)[0]
				return min(x1, x2, y1, y2), max(x1, x2, y1, y2)
			init = view.text_to_layout(sel[0].a)[0], view.text_to_layout(sel[0].b)[0]
			left, right = reduce(func, sel, init)

			# methods for scrolling to preserve horizontal margin
			align_left = lambda: scroll_to(horizontal=left - LEFT_DIST)
			align_right = lambda: scroll_to(horizontal=right + RIGHT_DIST - viewport_size[0])

			# distance of selection to left/right of viewport
			dist_left = left - viewport_position[0]
			dist_right = viewport_position[0] - right + viewport_size[0]

			# preserve the horizontal margin, maybe only at one side
			if viewport_size[0] - LEFT_DIST - RIGHT_DIST < right - left:
				# we can only preserve the horizontal margin at one side
				if multiple:
					pass # TODO: imitate sublime behaviour
				else:
					if sel[0].a <= sel[0].b: align_right()
					else: align_left()
			elif dist_left < LEFT_DIST: align_left()
			elif dist_right < RIGHT_DIST: align_right()


		if do_horizontal:
			preserve_horizontal_margin()

