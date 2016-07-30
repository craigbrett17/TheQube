# -*- coding: utf-8 -*-

from logger import logger
logging = logger.getChild('sessions.facebook.main')

from pydispatch import dispatcher
from utils.thread_utils import call_threaded
from utils.wx_utils import always_call_after

import application
import config
import global_vars
import interface
import core.gui
import misc
import oauth2
import output
import buffers
import gui
import sessions
import signals
import time
import wx
import BaseHTTPServer
import webbrowser
from base64 import b64encode, b64decode
from urlparse import urlparse, parse_qs
from string import maketrans
from json import dumps
from ast import literal_eval
from core.sessions.buffers  import Buffers
from session import Login
from core.sessions.hotkey.hotkey import Hotkey
from session import SpeechRecognition
from session import WebService
from facebook import GraphAPI

logged = False
verifier = None

class Handler(BaseHTTPServer.BaseHTTPRequestHandler):

 def do_GET(self):
  global logged
  self.send_response(200)
  self.send_header("Content-type", "text/html")
  self.end_headers()
  logged = True
  params = parse_qs(urlparse(self.path).query)
  global verifier
  verifier = params.get('oauth_verifier', [None])[0]
  self.wfile.write(_("You have successfully logged in to Facebook! Your friends await!"))
  self.wfile.close()

class Facebook(Buffers, Hotkey, WebService):

    def __init__(self, *args, **kwargs):
        super(Facebook, self).__init__(*args, **kwargs)
        self.users = {}
        self.qube_facebook_token = self.retrieve_facebook_token()
        success = self.do_login()
        if success:
            self.login_succeeded()
            self.post_update("Test post from the Qube")
        else:
            self.login_failed()

    def register_default_buffers(self):
        if not self.online and not self.config['security']['workOffline']:
            return logging.debug("Avoiding buffer registration as offline mode is currently disabled.")
        logging.info("%s: Registering default buffers..." % self.name)  
        super(Facebook, self).register_default_buffers()
        #Hold buffer names in strings for translators
        [_('News Feed'), _('Most Recent')]
        self.register_buffer("News Feed", buffers.news_feed, announce=False, set_focus=False)
        #self.register_buffer("Most Recent", buffers.news_feed, announce=False, set_focus=False)
        self.default_buffer = self.get_buffer_by_name('News Feed')
        if not self.buffer_metadata.has_key('current'):
            self.buffer_metadata['current'] = 1
        if self.buffer_metadata['current'] >= len(self.buffers):
             self.buffer_metadata['current'] = 1
        self.set_buffer(self.buffer_metadata['current'], False)

    def retrieve_facebook_token(self):
        fbDataOrig = str(self.config['oauth']['fbData'])
        return fbDataOrig
 
    def do_login(self, *args, **kwargs):
        self.graph_api = GraphAPI(self.qube_facebook_token)
        resp = self.api_call('get_object', _("verifying your Facebook credentials"), id="me")
        self.username = (resp["name"]);
        return True

    def login_succeeded(self):
        self.save_config()
        output.speak(_("Logged into Facebook as %s") % self.username)
        self.API_initialized()
  
    def login_failed(self):
        output.speak(_("Login failed!"), True)

    def post_update(self, text=u"", buffer=None, index=None):
        try:
            self.api_call('put_wall_post', _("Post"), message=text.encode("UTF-8"))
            self.play(self.config['sounds']['tweetSent'])
        except:
            return wx.CallAfter(self.interface.NewPost, buffer=buffer, index=index, text=text)

    def api_call(self, call_name, action="", report_success=True, report_failure=True, wait_for_connection=False, preexec_message="", login=False, *args, **kwargs):
        #Make a call to Facebook
        if preexec_message:
            output.speak(preexec_message, True)
        try:
            val = getattr(self.graph_api, call_name)(*args, **kwargs)
        except Exception as e:
            logging.exception("%s: Error making call to Facebook API function %s: %s" % (self.name, call_name, e.message))
            if report_failure and hasattr(e, 'reason'):
                output.speak(_("%s failed.  Reason: %s") % (action, e.reason))
            raise
        if report_success:
            output.speak(_("%s succeeded.") % action)
        return val