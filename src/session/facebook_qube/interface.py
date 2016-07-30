# -*- coding: utf-8 -*-

from logger import logger
logging = logger.getChild('sessions.facebook.interface')

from durus_importer import SessionImporter
from core.sessions.buffers.buffer_defaults import buffer_defaults
from utils.delay import delay_action
from utils.thread_utils import call_threaded
from utils.wx_utils import modal_dialog, question_dialog
from geopy.geocoders import GoogleV3

import config
import calendar
import core.gui
import global_vars
import misc
import os
import output
import paths
import rfc822
import buffers
import gui
import sessions
import templates
import time
import wx
import traceback
from core.sessions.buffers.interface import BuffersInterface
from core.sessions.hotkey.interface import HotkeyInterface
from meta_interface import MetaInterface

class FacebookInterface (BuffersInterface, HotkeyInterface, MetaInterface):
    @buffer_defaults
    def NewPost(self, buffer=None, index=None, text=u"", title=None):
        """
        Allows you to post a new status
        """
        new = gui.NewTweetDialog(parent=self.session.frame, text=text, title=title)
        new.retweet.Show(retweet)
        new.quote.Show(quote)
        new.message.SetInsertionPoint(0)
        val=new.ShowModal()
        if val==wx.ID_OK:
            text = new.message.GetValue()
        else:
            logging.debug("User canceled post.")
            return output.speak(_("Canceled."), True)
        call_threaded(self.session.post_update, text=text)

# for this module, assign interface to be FacebookInterface
interface = FacebookInterface