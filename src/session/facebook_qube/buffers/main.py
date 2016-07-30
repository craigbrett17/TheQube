# -*- coding: utf-8 -*-

from logger import logger
logging = logger.getChild('sessions.facebook.buffers.main')

from pydispatch import dispatcher
from core.sessions.buffers.buffer_defaults import buffer_defaults

import calendar
import config
import html_filter
import misc
import output
import re
import rfc822
import signals
import time
import wx
from utils.wx_utils import question_dialog
from conditional_template import ConditionalTemplate as Template

from core.sessions.buffers.buffers import Updating
from core.sessions.storage.buffers.storage import Storage
from core.sessions.sound.buffers.audio import Audio
from core.sessions.buffers import field_metadata as meta

class Facebook (Updating, Storage, Audio):
    """Parent Facebook buffer class."""

    def __init__ (self, *args, **kwargs):
        super(Facebook, self).__init__(*args, **kwargs)
        self.set_flag('deletable', False)
        self.set_flag('temp', False)
        self.set_flag('filterable', True)
        self.set_flag('exportable', True)

    @staticmethod
    def standardize_timestamp(date):
        if date is None:
            return None
        return calendar.timegm(rfc822.parsedate(date))

    def process_update(self, update, *args, **kwargs):
        update = self.find_new_data (update)
        update.reverse()
        for i in update:
            if 'text' in i:
                i['text'] = html_filter.StripChars(i['text'])
            return update