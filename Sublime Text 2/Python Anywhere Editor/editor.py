import sublime, sublime_plugin
import datetime, os, re
import tempfile
from BeautifulSoup import BeautifulSoup

PLUGIN_NAME = "PythonAnywhereEditor"
SETTINGS_FILENAME = "%s.sublime-settings" % PLUGIN_NAME
TMP_DIR = tempfile.gettempdir()

THREAD_PING = 10
FRAMES_PER_PING = 7
PROGRESS_FRAMES = [
    '><{{">    ',
    ' ><{{">   ',
    '  ><{{">  ',
    '   ><{{"> ',
    '    ><{{">',
    '    <"}}><',
    '   <"}}>< ',
    '  <"}}><  ',
    ' <"}}><   ',
    '<"}}><    ',
]

import service

settings = sublime.load_settings(SETTINGS_FILENAME)
log_panel = None
next_command = []
in_process = False

def check_in_process(fn):
    '''decorator for checking if we in processing with hosting'''
    def wrapped(*args, **kwargs):
        if in_process:
            return
        return fn(*args, **kwargs)
    return wrapped

def processing(show_animation=True, autorun_next_command=True):
    '''decorator for progress animation'''
    def decorator(fn):
        def wrapped(self, thread, *args, **kwargs):
            global in_process
            in_process = True
            counter = int(kwargs.pop('counter', 0))
            if thread.is_alive():
                if show_animation and counter % FRAMES_PER_PING == 0:
                    frame_index = counter / FRAMES_PER_PING % len(PROGRESS_FRAMES)
                    frame = PROGRESS_FRAMES[frame_index]
                    anim_str = " %s " % frame
                    log(anim_str, timestamp=False, new_line=False,
                        replace_last=len(anim_str) if counter else 0)
                sublime.set_timeout(
                    lambda: wrapped(self, thread, *args, counter=counter+1, **kwargs),
                    THREAD_PING)
            else:
                in_process = False
                if show_animation:
                    log(" ... ", timestamp=False, new_line=False,
                        replace_last=(len(PROGRESS_FRAMES[0]) + 2) if counter else 0)
                if thread.error:
                    clear_commands()
                    log(thread.error, timestamp=False)
                else:
                    fn(self, thread, *args, **kwargs)
                    if autorun_next_command:
                        run_next_command()
        return wrapped
    return decorator

def username_required(next):
    '''decorator for username prompt if not exist'''
    def decorator(fn):
        def wrapped(self, *args, **kwargs):
            username = settings.get("username")
            if not username:
                next_command.append(next)
                sublime.active_window().run_command("prompt_python_anywhere_username")
            else:
                fn(self, *args, **kwargs)
        return wrapped
    return decorator

def login_required(next):
    '''decorator for login prompt if not exist'''
    def decorator(fn):
        def wrapped(*args, **kwargs):
            username = settings.get("username")
            if not username:
                next_command.append(next)
                sublime.active_window().run_command("prompt_python_anywhere_username")
            elif not service.is_logged_in():
                next_command.append(next)
                sublime.active_window().run_command("prompt_python_anywhere_login")
            else:
                fn(*args, **kwargs)
        return wrapped
    return decorator


class PromptPythonAnywhereUsername(sublime_plugin.WindowCommand):
    def run(self):
        username = settings.get("username")
        if not username:
            username = ""
        self.window.show_input_panel("Username:", username,
            self.on_done, None, clear_commands)

    def on_done(self, new_username):
        if not new_username:
            self.run()
            return
        old_username = settings.get('username')
        if old_username != new_username:
            settings.set("username", new_username)
            sublime.save_settings(SETTINGS_FILENAME)
            service.clear_cookie()
        run_next_command()

class PromptPythonAnywhereLogin(sublime_plugin.WindowCommand):
    @username_required("prompt_python_anywhere_login")
    @check_in_process
    def run(self):
        self.window.show_input_panel("Password:", "",
            self.on_done, None, clear_commands)

    def on_done(self, password):
        if not password:
            self.run()
            return
        log("login", new_line=False)
        username = settings.get("username")
        thread = service.LoginThread(
            kwargs=dict(username=username, password=password))
        thread.start()
        self.handle_thread(thread)

    @processing()
    def handle_thread(self, thread):
        log("success", timestamp=False)

class PromptPythonAnywhereNewFile(sublime_plugin.WindowCommand):
    @login_required("prompt_python_anywhere_new_file")
    @check_in_process
    def run(self):
        username = settings.get("username")
        last_opened_file = settings.get("last_opened_file")
        if last_opened_file:
            last_opened_file = os.path.dirname(last_opened_file + "/")
        else:
            last_opened_file = "home/%s/" % username

        self.window.show_input_panel("New File /", last_opened_file,
            self.on_done, None, clear_commands)

    def on_done(self, file_path):
        file_path = file_path.lstrip("/\\")
        settings.set("last_opened_file", file_path)
        sublime.save_settings(SETTINGS_FILENAME)

        filename = os.path.basename(file_path)
        if not filename:
            log("cann't catch filename from path /%s" % file_path)
            return
        dirname = os.path.dirname(file_path)

        log("new file /%s" % file_path, new_line=False)

        username = settings.get("username")
        thread = service.NewFileThread(
            kwargs=dict(username=username, dirname=dirname, filename=filename))
        thread.start()
        self.handle_thread(thread, file_path)

    @processing()
    def handle_thread(self, thread, file_path):
        log("success", timestamp=False)
        open_tmp_file(self.window, file_path)

class PromptPythonAnywhereOpenFile(sublime_plugin.WindowCommand):
    @login_required("prompt_python_anywhere_open_file")
    @check_in_process
    def run(self):
        username = settings.get("username")
        last_opened_file = settings.get("last_opened_file")
        if not last_opened_file:
            last_opened_file = "home/%s/" % username

        self.window.show_input_panel("Open File /", last_opened_file,
            self.on_done, None, clear_commands)

    def on_done(self, file_path):
        file_path = file_path.lstrip("/\\")
        settings.set("last_opened_file", file_path)
        sublime.save_settings(SETTINGS_FILENAME)

        log("open file /%s" % file_path, new_line=False)

        username = settings.get("username")
        thread = service.OpenFileThread(
            kwargs=dict(username=username, file_path=file_path))
        thread.start()
        self.handle_thread(thread, file_path)

    @processing()
    def handle_thread(self, thread, file_path):
        if thread.result == None:
            log("something gone wrong", timestamp=False)
        else:
            log("success", timestamp=False)
            open_tmp_file(self.window, file_path, thread.result)

class PythonAnywhereSyncFile(sublime_plugin.TextCommand):
    @login_required("python_anywhere_sync_file")
    def run(self, edit):
        if self.view.settings().get("is_python_anywhere_file"):
            self.sync(edit)

    def sync(self, edit):
        file_path = self.view.settings().get("python_anywhere_file_path")

        username = settings.get("username")
        thread = service.OpenFileThread(
            kwargs=dict(username=username, file_path=file_path))
        thread.start()

        self.handle_thread(thread, edit, file_path)

    @processing(False)
    def handle_thread(self, thread, edit, file_path):
        if thread.result == None:
            log("something gone wrong while syncing /%s" % file_path)
        else:
            log("synced /%s" % file_path)

            visible_region = self.view.visible_region()
            viewport = self.view.viewport_position()
            sel = [r for r in self.view.sel()]

            self.view.replace(edit, sublime.Region(0, self.view.size()),
                thread.result)

            self.view.sel().clear()
            for r in sel:
                self.view.sel().add(r)
            sublime.set_timeout(
                lambda: self.view.set_viewport_position(viewport, False), 1)

            self.view.settings().set("python_anywhere_dont_save_me", True)
            self.view.run_command("save")

class PythonAnywhereSyncOpenedFiles(sublime_plugin.WindowCommand):
    @login_required("python_anywhere_sync_opened_files")
    def run(self):
        log("sync opened files")
        for window in sublime.windows():
            for view in window.views():
                view.run_command("python_anywhere_sync_file")

class PythonAnywhereEventListener(sublime_plugin.EventListener):
    @check_in_process
    def on_post_save(self, view):
        if view.settings().has("python_anywhere_dont_save_me"):
            view.settings().erase("python_anywhere_dont_save_me")
            return
        if view.settings().get("is_python_anywhere_file"):
            self.save(view)

    @login_required("save")
    def save(self, view):
        file_path = view.settings().get("python_anywhere_file_path")
        content = view.substr(sublime.Region(0, view.size()))

        log("save file /%s" % file_path, new_line=False)

        username = settings.get("username")
        thread = service.SaveFileThread(
            kwargs=dict(username=username, file_path=file_path, content=content))
        thread.start()
        self.handle_thread(thread)

    @processing()
    def handle_thread(self, thread):
        log("success", timestamp=False)

    def on_close(self, view):
        if not view.settings().get("is_python_anywhere_file"):
            return
        file_path = view.settings().get("python_anywhere_file_path")
        tmp_file_path = os.path.join(PLUGIN_NAME, file_path)
        # remove file
        try:
            curdir = os.getcwd()
            os.chdir(TMP_DIR)
            os.remove(tmp_file_path)
        except Exception, e:
            log("error while delete temp file /%s: %s" % (file_path, e))
        # trying remove all temp path if no have any temp files
        try:
            os.removedirs(os.path.dirname(tmp_file_path))
        except:
            pass
        finally:
            os.chdir(curdir)

class PythonAnywhereWebAppsList(sublime_plugin.WindowCommand):
    @login_required("python_anywhere_web_apps_list")
    def run(self):
        log("load web apps list", new_line=False)
        username = settings.get("username")
        thread = service.WebAppsListThread(kwargs=dict(username=username))
        thread.start()
        self.handle_thread(thread)

    @processing(autorun_next_command=False)
    def handle_thread(self, thread):
        if thread.result == None:
            log("something gone wrong while getting web apps list", timestamp=False)
        else:
            # parse web apps list
            soup = BeautifulSoup(thread.result)
            web_apps_list = [
                li.contents[1].strip()
                for li in soup(['a'], href=re.compile(r'^#id_'))[0:-1]
            ]
            extract_id_rx = re.compile(r'webapps/(.*?)/')
            web_apps_ids = [
                re.search(extract_id_rx, f['action']).group(1)
                for f in soup(['form'], {"class": "reload_web_app"})
            ]

            # save web apps ids in class variable
            self.web_apps_ids = web_apps_ids

            # if we have more then one web app, then show quick select panel
            if len(web_apps_ids) > 1:
                log("success", timestamp=False)
                self.window.show_quick_panel(
                    [
                        [i[1], "Web App ID: %s" % i[0]]
                        for i in zip(web_apps_ids, web_apps_list)
                    ],
                    self.on_choose_app
                )
            else:
                log("success (web app id: %s)" % web_apps_ids[0], timestamp=False)
                self.on_choose_app(0)

    def on_choose_app(self, index):
        settings.set("web_app_id", self.web_apps_ids[index])
        sublime.save_settings(SETTINGS_FILENAME)
        run_next_command()

class PythonAnywhereReload(sublime_plugin.WindowCommand):
    @login_required("python_anywhere_reload")
    def run(self):
        web_app_id = settings.get("web_app_id")
        if not web_app_id:
            next_command.append("python_anywhere_reload")
            sublime.active_window().run_command("python_anywhere_web_apps_list")
            return

        log("reload web apps", new_line=False)
        username = settings.get("username")
        thread = service.ReloadWebAppsThread(kwargs=dict(username=username,
            web_app_id=web_app_id))
        thread.start()
        self.handle_thread(thread)

    @processing()
    def handle_thread(self, thread):
        log("success", timestamp=False)


def log(text, timestamp=True, new_line=True, replace_last=0):
    if timestamp:
        text = "[%s] %s" % (datetime.datetime.now(), text)
    if new_line:
        text = "%s\n" % text
    text = str(text)

    global log_panel
    if not log_panel:
        log_panel = sublime.active_window().get_output_panel(PLUGIN_NAME)

    e = log_panel.begin_edit()
    if replace_last:
        log_panel.replace(e,
            sublime.Region(log_panel.size() - replace_last, log_panel.size()),
            text)
    else:
        log_panel.insert(e, log_panel.size(), text)
    log_panel.end_edit(e)

    sublime.active_window().run_command("show_panel",
        dict(panel="output.%s" % PLUGIN_NAME))
    log_panel.show(log_panel.size())

def get_tmp_file_path(file_path):
    tmp_dir = tempfile.gettempdir()
    if file_path[0] == "/":
        file_path_rel = file_path[1:]
    return os.path.join(tmp_dir, PLUGIN_NAME, file_path_rel)

def create_tmp_file(file_path, content=None):
    file_path_abs = os.path.join(TMP_DIR, PLUGIN_NAME, file_path)
    if not os.path.exists(os.path.dirname(file_path_abs)):
        os.makedirs(os.path.dirname(file_path_abs))
    try:
        f = open(file_path_abs, "w")
        if content != None:
            f.write(content)
        f.close()
    except Exception, e:
        log("cann't create temp file %s: %s" % (file_path_abs, e))
        return
    return file_path_abs

def open_tmp_file(window, file_path, content=None):
    file_path_abs = create_tmp_file(file_path, content)
    if not file_path_abs:
        return
    v = window.open_file(file_path_abs)
    s = v.settings()
    s.set("is_python_anywhere_file", True)
    s.set("python_anywhere_file_path", file_path)

def run_next_command():
    if not next_command:
        return
    sublime.active_window().run_command(next_command.pop())

def clear_commands():
    global next_command
    next_command = []
