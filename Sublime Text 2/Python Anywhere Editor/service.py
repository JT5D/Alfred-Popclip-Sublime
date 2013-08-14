import cookielib
import editor
import re
import threading
import urllib, urllib2

USER_AGENT = "SublimeText2 - %s" % editor.PLUGIN_NAME
BASE_URL = "https://www.pythonanywhere.com"
LOGIN_URL = BASE_URL + "/login/"
FILES_URL = BASE_URL + "/user/%s/files/%s"
WEB_APPS_LIST_URL = BASE_URL + "/user/%s/webapps/"
WEB_APP_RELOAD_URL = BASE_URL + "/user/%s/webapps/%s/reload"

class NoRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        infourl = urllib.addinfourl(fp, headers, req.get_full_url())
        infourl.status = code
        infourl.code = code
        return infourl
    http_error_300 = http_error_302
    http_error_301 = http_error_302
    http_error_303 = http_error_302
    http_error_307 = http_error_302

cookie_handler = urllib2.HTTPCookieProcessor()
opener = urllib2.build_opener(NoRedirectHandler(), cookie_handler)
opener.addheaders = [('User-Agent', USER_AGENT)]

class BackgroundThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        self.result = None
        self.error = None
        super(BackgroundThread, self).__init__(*args, target=self.process, **kwargs)

    def run(self, *args, **kwargs):
        try:
            super(BackgroundThread, self).run(*args, **kwargs)
        except Exception, e:
            self.error = e

    def process(self):
        pass

class LoginThread(BackgroundThread):
    def process(self, username, password):
        result = opener.open(LOGIN_URL)
        csrftoken = None
        for cookie in cookie_handler.cookiejar:
            if cookie.name == "csrftoken":
                csrftoken = cookie.value

        req = urllib2.Request(LOGIN_URL)
        req.data = urllib.urlencode(dict(
            csrfmiddlewaretoken=csrftoken,
            username=username,
            password=password))
        req.headers = dict(Referer=LOGIN_URL)
        result = opener.open(req)

        if result.info().get('location', '').startswith(BASE_URL + "/login"):
            clear_cookie()
            raise Exception, "invalid username or password"

class NewFileThread(BackgroundThread):
    def process(self, username, dirname, filename):
        result = opener.open(FILES_URL % (username, dirname),
            urllib.urlencode(dict(filename=filename)))
        check_result(result)

class OpenFileThread(BackgroundThread):
    def process(self, username, file_path):
        result = opener.open(FILES_URL % (username, file_path))
        self.result = check_result(result)

class SaveFileThread(BackgroundThread):
    def process(self, username, file_path, content):
        result = opener.open(FILES_URL % (username, file_path),
            urllib.urlencode(dict(new_contents=content)))
        check_result(result)

class WebAppsListThread(BackgroundThread):
    def process(self, username):
        result = opener.open(WEB_APPS_LIST_URL % username)
        self.result = check_result(result)

class ReloadWebAppsThread(BackgroundThread):
    def process(self, username, web_app_id):
        result = opener.open(WEB_APP_RELOAD_URL % (username, web_app_id))
        check_result(result)


def is_logged_in():
    return bool(cookie_handler.cookiejar)

def clear_cookie():
    cookie_handler.cookiejar.clear()

def check_result(result):
    if result.info().get('location', '').startswith(BASE_URL + "/login"):
        clear_cookie()
        raise Exception, "cookie expired, relogin please"
    content = result.read()
    error_match = re.match(r'.*<div.*?id_error_message.*?>(.*?)</div>.*',
        content, re.S)
    if error_match:
        raise Exception, error_match.group(1).strip()
    return content
