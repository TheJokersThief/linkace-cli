from linkace_cli.api.base import APIBase

from linkace_cli import models
from linkace_cli.api.tags import Tags
from linkace_cli.api.lists import Lists


class Search(APIBase):
    def __init__(self, base_url, api_token):
        super(Search, self).__init__(base_url, api_token)
        self.tags = Tags(base_url, api_token)
        self.lists = Lists(base_url, api_token)

    def get_links_by_tag_exact(self, tag_id: int):
        return self.tags.links(tag_id)

    def get_links_by_tag_query(self, query: str):
        tag_ids = self.api.get('search/tags', {'query': query})

        print(tag_ids)

        links = []
        for tag_id in tag_ids.keys():
            links.extend(self.tags.links(tag_id))

        # Deduplicate results based on ID
        return list({v['id']: v for v in links}.values())

    def get_links_by_list_exact(self, list_id: int):
        return self.lists.links(list_id)

    def get_links_by_list_query(self, query: str):
        list_ids = self.api.get('search/lists', {'query': query})

        links = []
        for list_id in list_ids:
            links.extend(self.lists.links(list_id))

        # Deduplicate results based on ID
        return list({v['id']: v for v in links}.values())

    def get_links_by_query(self, query: str):
        params = {
            'query': query,
            'search_title': query,
        }
        resp = self.api.get('search/links', params=params)
        resp = models.LinksPagination().load(resp)

        links = resp['data']
        while(resp['next_page_url']):
            resp = models.LinksPagination().load(self.api.get(resp['next_page_url']))
            links.extend(resp['data'])
        return links
