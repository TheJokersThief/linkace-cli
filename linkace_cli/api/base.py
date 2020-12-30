from linkace_cli.api import LinkAce


class APIBase():
    api = None

    def __init__(self, base_url, api_token):
        self.api = LinkAce(base_url, api_token)
