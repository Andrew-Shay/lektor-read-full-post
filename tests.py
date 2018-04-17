
from lektor_read_full_post import ReadFullPostPlugin

SPLIT_ONE = "[//]: # (PLUGIN-READ-FULL-POST)"
SPLIT_TWO = "<!-- PLUGIN-READ-FULL-POST -->"

URL_PATH = "https://localhost"


class MockSource(object):

    def __init__(self):
        self.source = ""


class MockPost(object):

    def __init__(self):

        self.url_path = URL_PATH
        self._data = {
            'body': MockSource()
        }


def get_post(text):
    post = MockPost()
    post._data['body'].source = text

    return post


def clean_up():
    """
    Reset ReadFullPostPlugin class
    """
    ReadFullPostPlugin.rfp_link_text = ''
    ReadFullPostPlugin.rfp_always_display = ''
    ReadFullPostPlugin.rfp_split_text = []


class TestRfpProcessPost(object):

    def setup(self):
        ReadFullPostPlugin.rfp_process_config(None, None, None)

    def teardown(self):
        clean_up()

    def test_default_split_one(self):

        text = "Hello\nworld\n{}\nfoo\nbar".format(SPLIT_ONE)
        post = get_post(text)
        expected_full = "Hello\nworld\nfoo\nbar"
        expected_short = "Hello\nworld[<br><br>Read Full Post]({})".format(URL_PATH)

        result = ReadFullPostPlugin.rfp_process_post(post)

        assert result._data['body'].source == expected_full
        assert result._data['body_short'].source == expected_short