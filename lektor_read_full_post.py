# -*- coding: utf-8 -*-

# Read Full Post Lektor Plugin created by Andrew Shay. https://andrewshay.me

from copy import deepcopy

from lektor.pluginsystem import Plugin


class ReadFullPostPlugin(Plugin):
    name = "Read Full Post"
    description = "Allows blog listing posts to be shortened with a link to the full post."

    rfp_config = {}

    @classmethod
    def rfp_always_display(cls):
        return cls.rfp_config['always-display'].lower() == 'true'

    @classmethod
    def rfp_spilt_text(cls, body_type):
        split_text = cls.rfp_config["{}-split-text".format(body_type)]
        split_text = "\n{}\n".format(split_text)
        return split_text

    @classmethod
    def rfp_link_text(cls, body_type, url):
        link_text = cls.rfp_config["{}-link-text".format(body_type)]
        link_text = link_text.format(URL_PATH=url)
        return link_text

    @classmethod
    def rfp_process_post(cls, post):
        body_type = post.datamodel.field_map['body'].type.name
        post._data['body_short'] = deepcopy(post._data['body'])
        text_full = post._data['body'].source

        split_text = cls.rfp_spilt_text(body_type)
        contains_split = split_text in text_full
        if contains_split:
            split = text_full.split(split_text)
            post._data['body_short'].source = split[0]
            post._data['body'].source = '  \n'.join(split)

        if cls.rfp_always_display() or contains_split:
            post._data['body_short'].source += cls.rfp_link_text(body_type, post.url_path)

        return post

    def on_setup_env(self, **extra):
        ReadFullPostPlugin.rfp_config = self.get_config()

        self.env.jinja_env.globals.update(plugin_read_full_post=ReadFullPostPlugin.rfp_process_post)
