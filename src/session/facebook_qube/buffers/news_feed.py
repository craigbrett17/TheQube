from logger import logger
logging = logger.getChild('sessions.facebook.buffers.home')

import threading

from posts import Posts

class news_feed(Posts):
    """Any of the news feed type buffers"""

    def __init__ (self, *args, **kwargs):
        self.init_done_event = threading.Event()
        super(news_feed, self).__init__(*args, **kwargs)
        self.item_name = _("post")
        self.item_name_plural = _("posts")
        self.item_sound = self.session.config['sounds']['tweetReceived']
        self.init_done_event.set()