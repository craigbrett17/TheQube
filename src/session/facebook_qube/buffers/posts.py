# -*- coding: utf-8 -*-

from main import Facebook
from core.sessions.buffers import field_metadata as meta
from core.sessions.buffers.buffer_defaults import buffer_defaults

class Posts(Facebook):
    """Base class for all Facebook post buffers."""

    primary_key = 'id'

    def __init__(self, *args, **kwargs):
        super(Posts, self).__init__(*args, **kwargs)
        #And the template:
        self.default_template = 'default_template'