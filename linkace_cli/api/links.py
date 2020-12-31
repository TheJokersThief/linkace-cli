from linkace_cli.api.base import APIBase
from linkace_cli import models


class Links(APIBase):
    """CRUD interaction for all things link-based"""
    def get(self, id: int = None, order_by: models.OrderBy = None, order_dir: models.OrderDir = None):
        """
        Get all links or a single link's details. The order can be modified using the enums in models.

        If a numeric ID for a link is provided, it will only return details for that link.
        """
        order_dir = order_dir.value if order_dir else None
        order_by = order_by.value if order_by else None

        if not id:
            resp = self.api.get('links', {'order_by': order_by, 'order_dir': order_dir})
            resp = models.LinksPagination().load(resp)

            links = resp['data']
            while(resp['next_page_url']):
                resp = models.LinksPagination().load(self.api.get(resp['next_page_url']))
                links.extend(resp['data'])
            return links
        return models.Link().load(self.api.get(f'links/{id}'))

    def create(self, link: models.Link):
        return self.api.post('links', link)

    def delete(self, id: int):
        return self.api.delete(f'links/{id}')

    def update(self, id: int, link: models.Link):
        return self.api.patch(f'links/{id}', link)
