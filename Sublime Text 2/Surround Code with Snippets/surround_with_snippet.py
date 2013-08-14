"""
This plugin allows you to surround selected text with snippets

Author            : ask
Email             : a.skurihin@gmail.com
Version           : 0.2
Last modification : 17.09.2011

"""
from os.path import basename, dirname
from os.path import join as join_path
import os
import re
import xml.dom.minidom
from contextlib import contextmanager

import sublime
import sublime_plugin


@contextmanager
def selection(view):
    region = expand_to_lines(view)
    selected_text = region_text(view, region).split('\n')
    ind_lvl = len(selected_text[0]) - len(selected_text[0].lstrip())
    indention = selected_text[0][0:ind_lvl]
    yield {'selected_lines': selected_text, 'indention': indention}


def expand_to_lines(view):
    """Adjust the selection to capture the whole lines
    also correct selection if cursor placed on the next line"""
    r = expand_selection(view)
    empty_line_correction = region_text(view, r).split('\n').count('')
    r = sublime.Region(r.begin(), r.end() - empty_line_correction)
    view.sel().clear()
    view.sel().add(r)
    return r


def expand_selection(view):
    view.run_command('expand_selection', {'to': 'line'})
    return view.sel()[0]


def handle_template(text_to_replace, snippet_file, indention):
    """Open snippet file and replace last cursor stop by text_to_replace saving indention level"""
    def replace(match_obj):
        indention = match_obj.group(1)
        unindented = lstrip(text_to_replace)
        to_replace = [indention + escape(x) for x in unindented]
        return '\n'.join(to_replace)

    pattern = "([ \t]+)?\${\d:\$SELECTION}"
    template = parse_template(snippet_file)
    template_replaced = re.sub(pattern, replace, template, 1)
    template_replaced_indented = indent(template_replaced, indention)
    return template_replaced_indented


def indent(to_indent, indention):
    """Insert indention for each str in a given list"""
    to_indent = to_indent.split('\n')
    indented = [indention + x for x in to_indent]
    return '\n'.join(indented)


def lstrip(list):
    "Remove leading whitespaces but save code structure"
    while list[0].startswith(' '):
        list = [x.replace(" ", "", 4) for x in list]
    return list


def parse_template(template_path):
    "Parse and clean a template"
    dom = xml.dom.minidom.parse(template_path)
    template = dom.lastChild.getElementsByTagName('content')[0].firstChild.nodeValue
    return template.strip()


def escape(string):
    """Escape special charecters in line start with slash"""
    return string.replace('\\', '\\\\')


def region_text(view, region):
    return view.substr(region)

is_snippet = lambda s: s.endswith(".sublime-snippet")


class SurroundWithSnippetCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.snippet_list = self.get_snippet_list()
        self.show_panel(self.on_choise_insert_snippet)

    def get_snippet_list(self):
        prefix = sublime.packages_path()
        file_type = basename(dirname(self.view.settings().get('syntax')))
        self.path = join_path(prefix, file_type)
        return filter(is_snippet, os.listdir(self.path))

    def show_panel(self, callback):
        snippet_names = [x.split('.sublime-snippet')[0] for x in self.get_snippet_list()]
        self.view.window().show_quick_panel(snippet_names, callback)

    def on_choise_insert_snippet(self, choise):
        with selection(self.view) as s:
            if choise == -1:
                return
            snippet_file = join_path(self.path, self.snippet_list[choise])
            snippet = handle_template(s['selected_lines'], snippet_file, s['indention'])
            self.view.run_command("insert_snippet", {"contents": snippet})
