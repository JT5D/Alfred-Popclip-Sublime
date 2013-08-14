import sublime, sublime_plugin
import os, re
import plistlib
from xml.etree import ElementTree
from zipfile import ZipFile

snippets = []

whitespace = re.compile('\s+')

class Snippet:
	def __init__(self, desc, content, tab, scopes):
		self.desc = desc
		self.code = content
		self.tab = tab
		self.scopes = scopes
	
	def preview(self):
		preview = ''
		code = self.code

		parse_max = 80
		return_max = 60

		l = min(len(code), parse_max)
		i = 0
		escape = False
		brackets = 0
		while i < l:
			c = code[i]
			i += 1
			if c == '$' and not escape:
				if i < l:
					n = code[i]
					if n.isdigit() or n == '{':
						if n.isdigit():
							i += 1
							while i < l and code[i].isdigit():
								i += 1
						else:
							brackets += 1
							while i < l and code[i] not in ':}':
								i += 1

							i += 1
			elif c == '}' and brackets > 0 and not escape:
				brackets -= 1
			elif c == '\\' and not escape:
				escape = True
			else:
				escape = False
				preview += c

		preview = whitespace.sub(' ', preview).strip()
		word_boundary = preview[:return_max].rsplit(' ', 1)[0]
		if len(word_boundary) > return_max or len(preview) < return_max:
			return word_boundary
		else:
			return preview[:return_max]

def parse_snippet(f, ext):
	if ext == '.sublime-snippet':
		tree = ElementTree.parse(f)

		desc = tree.find('description').text
		content = tree.find('content').text
		trigger = tree.find('tabTrigger').text
		scope = tree.find('scope').text.split(', ')

	elif ext == '.tmSnippet':
		plist = plistlib.readPlist(f)
		desc = plist['name']
		content = plist['content']
		trigger = plist['tabTrigger']
		scope = plist['scope']
	
	return Snippet(desc, content, trigger, scope)

def read_zip(path):
	results = []
	zipf = ZipFile(path, 'r')
	for name in zipf.namelist():
		ext = os.path.splitext(name)[-1]
		if ext in ('.sublime-snippet', '.tmSnippet'):
			f = zipf.open(name, 'rb')
			results.append(parse_snippet(f, ext))
			f.close()
	
	return results

def find_snippets():
	global snippets

	new_snippets = []
	# Packages folder
	for root, dirs, files in os.walk(sublime.packages_path()):
		for name in files:
			try:
				ext = os.path.splitext(name)[-1]
				if ext in ('.sublime-snippet', '.tmSnippet'):
					path = os.path.join(root, name)
					f = open(path, 'rb')
					new_snippets.append(parse_snippet(f, ext))
					f.close()
				elif ext in ('.sublime-package', '.tmBundle'):
					new_snippets += read_zip(path)

			except:
				pass
	
	# Installed Packages
	for root, dirs, files in os.walk(sublime.installed_packages_path()):
		for name in files:
			try:
				ext = os.path.splitext(name)[-1]
				if ext == '.sublime-package':
					path = os.path.join(root, name)
					new_snippets += read_zip(path)
			except:
				pass

	snippets = new_snippets

find_snippets()

class Sniptastic(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		names = self.view.scope_name(view.sel()[0].b)
		scopes = []
		for name in names.split(' '):
			scope = []
			for section in name.split('.'):
				scope.append(section)
				scopes.append('.'.join(scope))

		candidates = []
		for s in snippets:
			for scope in s.scopes:
				if scope in scopes:
					candidates.append(s)

		items = [['%s { %s }' % (s.tab, s.desc), '\t' + s.preview()] for s in candidates]

		def callback(idx):
			if idx == -1: return # -1 means the menu was canceled
			view.run_command('insert_snippet', {'contents':candidates[idx].code})

		view.window().show_quick_panel(items, callback)
