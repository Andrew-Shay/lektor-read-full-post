# -*- coding: utf-8 -*-

# Read Full Post Lektor Plugin created by Andrew Shay

from copy import deepcopy

from lektor.pluginsystem import Plugin


class ReadFullPostPlugin(Plugin):
    name = 'Read Full Post'
    description = 'Allows blog listing posts to be shortened with a link to the full post.'
    link_text = "Read Full Post"
    always_display = True
    split_text = '[//]: # (PLUGIN-READ-FULL-POST)'

    @classmethod
    def plugin_read_full_post(cls, post):
        post._data['body_short'] = deepcopy(post._data['body'])
        text = post._data['body_short'].source

        text = text.split(cls.split_text)[0]

        if cls.always_display == 'true' or (cls.split_text in post._data['body'].source):
            text += "[{}]({})".format(cls.link_text, post.url_path)

        post._data['body_short'].source = text

        return post

    def on_setup_env(self, **extra):
        ReadFullPostPlugin.link_text = self.get_config().get('link-text')
        ReadFullPostPlugin.always_display = self.get_config().get('always-display')

        self.env.jinja_env.globals.update(
            plugin_read_full_post=self.plugin_read_full_post
        )
