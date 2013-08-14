import sublime, sublime_plugin

class SplitNavigationCommand(sublime_plugin.TextCommand):
	def run(self, edit, direction):
		win = self.view.window()
		num = win.num_groups()
		act = win.active_group()
		if direction == "up":
			act = act + 1
		else:
			act = act - 1
		win.focus_group(act % num)
		