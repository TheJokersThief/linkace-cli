from linkace_cli.api.base import APIBase
from linkace_cli import models


class Tags(APIBase):
    """CRUD interaction for all things tag-based"""
    def get(self, id: int = None, order_by: models.OrderBy = None, order_dir: models.OrderDir = None):
        """
        Get all tags or a single tag's details. The order can be modified using the enums in models.

        If a numeric ID for a tag is provided, it will only return details for that tag.
        """
        order_dir = order_dir.value if order_dir else None
        order_by = order_by.value if order_by else None

        if not id:
            resp = self.api.get('tags', {'order_by': order_by, 'order_dir': order_dir})
            resp = models.TagsPagination().load(resp)

            tags = resp['data']
            while(resp['next_page_url']):
                resp = models.TagsPagination().load(self.api.get(resp['next_page_url']))
                tags.extend(resp['data'])
            return tags
        return models.Tag().load(self.api.get(f'tags/{id}'))

    def create(self, tag: models.Tag):
        return self.api.post('tags', tag)

    def delete(self, id: int):
        return self.api.delete(f'tags/{id}')

    def update(self, id: int, tag: models.Tag):
        return self.api.patch(f'tags/{id}', tag)

    def links(self, id: int):
        resp = self.api.get(f'tags/{id}/links')
        resp = models.LinksPagination().load(resp)

        links = resp['data']
        while(resp['next_page_url']):
            resp = models.LinksPagination().load(self.api.get(resp['next_page_url']))
            links.extend(resp['data'])
        return links
