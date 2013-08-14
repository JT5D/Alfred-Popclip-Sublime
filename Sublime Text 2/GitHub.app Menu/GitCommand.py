import os
import subprocess

import sublime
import sublime_plugin
 

class GithubCommand(sublime_plugin.WindowCommand):  
    def run(self):  
        filename = self.window.active_view().file_name()
        dirname = os.path.dirname(filename)
        while dirname != '/':
            if '.git' in os.listdir(dirname):
                return subprocess.call(['open', '-a', 'GitHub', dirname])
            dirname = os.path.dirname(dirname)
        subprocess.call(['open', '-a', 'GitHub'])









