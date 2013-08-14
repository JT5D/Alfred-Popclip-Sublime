"""
TagWrapper plugin for Sublime Text 2
by Ignacy Sokolowski

"""
import re
import sublime
import sublime_plugin


# Regex for HTML tag names.
TAG_NAME_RE = re.compile(r'<(\w+)')
# Regex for HTML tags.
TAG_RE = re.compile(r'<[^>]*?>')


class TagWrapperInput(sublime_plugin.WindowCommand):
    """Shows input panel asking for HTML tag(s) to wrap selection in."""

    def is_enabled(self):
        return len(self.window.views()) > 0

    def run(self):
        """Show input panel."""
        self.window.show_input_panel(
            'Insert opening HTML tag(s):', '', self.on_done, None, None)

    def on_done(self, tag):
        """Execute tag_wrapper command with given tag as an argument."""
        self.window.active_view().run_command('tag_wrapper', {'tag': tag})


class TagWrapperCommand(sublime_plugin.TextCommand):
    """Wraps selection in HTML tags."""

    def run(self, edit, tag):
        # Finding all HTML tag names.
        tag_names = TAG_NAME_RE.findall(tag)
        if not tag_names:
            sublime.status_message('TagWrapper: invalid tag.')
            return
        # Creating closing tags.
        tag_end = ''.join(
            '</{0}>'.format(match) for match in reversed(tag_names)
        )

        for s in reversed(self.view.sel()):
            if s.empty():
                continue

            # Getting begining and end of selection.
            s_beg, s_end = s.begin(), s.end()

            # Wrapping selection in opening and closing HTML tags.
            self.view.insert(edit, s_beg, tag)
            self.view.insert(edit, s_end + len(tag), tag_end)


class StripTagsCommand(sublime_plugin.TextCommand):
    """Strips HTML tags from selection."""

    def run(self, edit):
        for s in reversed(self.view.sel()):
            if s.empty():
                continue

            # Getting selection region and contents.
            region = sublime.Region(s.begin(), s.end())
            contents = self.view.substr(region)

            # Stripping HTML tags.
            stripped = re.sub(TAG_RE, '', contents)
            self.view.replace(edit, region, stripped)
