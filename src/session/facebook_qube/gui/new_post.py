# -*- coding: utf-8

import sessions
import wx
import io

from core.gui import NewMessageDialog

class NewPostDialog(NewMessageDialog):
    def __init__(self, title=None, text=u"", *args, **kwargs):
        if title is None:
            title = _("Post")
        super(NewPostDialog, self).__init__(*args, title=title, **kwargs)
        self.setup_message_field(text)
        self.finish_setup()
        max_length = max_length or sessions.current_session.config['lengths']['tweetLength']