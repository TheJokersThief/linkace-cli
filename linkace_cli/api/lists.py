from linkace_cli.api.base import APIBase
from linkace_cli import models


class Lists(APIBase):
    """CRUD interaction for all things list-based"""
    def get(self, id: int = None, order_by: models.OrderBy = None, order_dir: models.OrderDir = None):
        """
        Get all lists or a single list's details. The order can be modified using the enums in models.

        If a numeric ID for a list is provided, it will only return details for that list.
        """
        order_dir = order_dir.value if order_dir else None
        order_by = order_by.value if order_by else None

        if not id:
            resp = self.api.get('lists', {'order_by': order_by, 'order_dir': order_dir})
            resp = models.ListsPagination().load(resp)

            lists = resp['data']
            while(resp['next_page_url']):
                resp = models.ListsPagination().load(self.api.get(resp['next_page_url']))
                lists.extend(resp['data'])
            return lists
        return models.List().load(self.api.get(f'lists/{id}'))

    def create(self, link: models.List):
        return self.api.post('lists', link)

    def delete(self, id: int):
        return self.api.delete(f'lists/{id}')

    def update(self, id: int, link: models.List):
        return self.api.patch(f'lists/{id}', link)

    def links(self, id: int):
        resp = self.api.get(f'lists/{id}/links')
        resp = models.LinksPagination().load(resp)

        links = resp['data']
        while(resp['next_page_url']):
            resp = models.LinksPagination().load(self.api.get(resp['next_page_url']))
            links.extend(resp['data'])
        return links
