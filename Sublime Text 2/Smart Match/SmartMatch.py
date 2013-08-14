#!/usr/bin/env python

# Copyright 2012 Craig Campbell
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import sublime, sublime_plugin

class SmartMatchCommand(sublime_plugin.TextCommand):
    def run(self, edit, character):
        new_selections = []

        for region in self.view.sel():
            if self.allowReplacement(region, character):
                if region.empty():
                    if region.begin() < self.view.size():
                        region = sublime.Region(region.begin(), region.begin()+1)
                    else:
                        region = sublime.Region(region.begin(), region.begin())
                    new_selections.append(region)
                else:
                    new_selections.append(region)
                continue

            new_selections.append(region)

        self.view.sel().clear()
        for sel in new_selections:
            self.view.sel().add(sel)
        self.view.run_command('insert',  {"characters": character})


    def allowReplacement(self, region, character):
        if region.size() > 1:
            return True

        start_char = {
            ']': '[',
            ')': '(',
            '}': '{'
        }

        # line
        line = self.view.line(region)

        # before
        text_before_insertion = self.view.substr(sublime.Region(line.begin(), region.begin()))
        open_count_before = text_before_insertion.count(start_char[character])
        close_count_before = text_before_insertion.count(character)

        if open_count_before - close_count_before  <= 0:
            return False

        # after
        text_after_insertion = ''
        position = region.end()-1
        while True:
            position += 1
            if position < self.view.size() and position < line.end():
                text = self.view.substr(sublime.Region(position, position+1))
                if text != character:
                    break
                else:
                    text_after_insertion += text
            else:
                break;
        if text_after_insertion == '':
            return False
        close_count_after = text_after_insertion.count(character)


        diff = (open_count_before - close_count_before) - close_count_after
        if diff == 0:
            return True
        else:
            return False

# TESTS -  put the cursor before "|" and type ")" character to test this package.

# function(|
# function(|)
# function(function(function(|))
# function(function(function(|)))
# function(function(function())|)
# function(function(function())|

# function(| ))))
# function(| ((((

# function(| )
# function(| (

# class().function(|)
# class(|).function()
# class((|).function()
# class(()).function(|)
# class((function(|))).function()
# class((function(|)).function()
# function().function(|)

# (((( |
# )))) |

# ( |
# ) |

# $(".meter-value").css("width", '.(round(($l/100)*$a|).'+"%");
