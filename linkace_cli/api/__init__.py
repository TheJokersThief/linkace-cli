import requests
from urllib.parse import urljoin
from urllib3.util import Retry

DEFAULT_TIMEOUT = 30  # seconds


class LinkAceHTTPSession(requests.Session):
    """
    Wrap a regular session to use a base URL and add a user-agent header
    """
    DEFAULT_USER_AGENT = "Linkace-CLI"

    def __init__(self, prefix_url, api_token, user_agent=None, *args, **kwargs):
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]

        super(LinkAceHTTPSession, self).__init__(*args, **kwargs)
        self.prefix_url = prefix_url

        if not user_agent:
            user_agent = LinkAceHTTPSession.DEFAULT_USER_AGENT

        self.headers.update({
            'Accept': 'application/json',
            'User-Agent': user_agent,
            'Authorization': f'Bearer {api_token}',
        })

    def request(self, method, url, *args, **kwargs):
        url = urljoin(self.prefix_url, url)
        return super(LinkAceHTTPSession, self).request(method, url, *args, **kwargs)


class LinkAce():
    """
    Make requests to the LinkAce API
    """
    def __init__(self, base_url, api_token, user_agent=None, enable_retries=True):
        self.site = LinkAceHTTPSession(base_url, api_token, user_agent=user_agent)

        if enable_retries:
            retry_strategy = Retry(
                total=3,
                status_forcelist=[429, 500, 502, 503, 504],
                backoff_factor=0.1
            )
            adapter = requests.adapters.HTTPAdapter(max_retries=retry_strategy)
            self.site.mount("http://", adapter)
            self.site.mount("https://", adapter)

    def get(self, url, params=None):
        req = self.site.get(url, params=params)
        req.raise_for_status()
        return req.json()

    def post(self, url, data=None):
        req = self.site.post(url, json=data)
        req.raise_for_status()
        return req.json()

    def patch(self, url, data=None):
        req = self.site.patch(url, json=data)
        req.raise_for_status()
        return req.json()

    def delete(self, url, data=None):
        req = self.site.delete(url, json=data)
        req.raise_for_status()
        return req.json()
