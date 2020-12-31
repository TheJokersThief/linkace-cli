#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import responses
import unittest

from linkace_cli.api.links import Links
from linkace_cli import models


class TestLinkAceAPI(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @responses.activate
    def test_link_get_all(self):
        with open('tests/fixtures/api/links_get_page1.json') as fixture:
            responses.add(responses.GET, 'http://example.com/api/v1/links',
                          json=json.load(fixture), status=200)

        with open('tests/fixtures/api/links_get_page2.json') as fixture:
            responses.add(responses.GET, 'http://example.com/api/v1/links',
                          json=json.load(fixture), status=200)

        api = Links("http://example.com/api/v1/", "Token-ABC")
        got = api.get(order_by=models.OrderBy.TITLE, order_dir=models.OrderDir.ASC)

        self.assertEqual(len(got), 2)
        self.assertEqual(got[0]['id'], 652)
        self.assertEqual(
            responses.calls[0].request.url,
            "http://example.com/api/v1/links?order_by=title&order_dir=asc"
        )

    @responses.activate
    def test_link_get_one(self):
        with open('tests/fixtures/api/links_get_one.json') as fixture:
            responses.add(responses.GET, 'http://example.com/api/v1/links/652',
                          json=json.load(fixture), status=200)
        api = Links("http://example.com/api/v1/", "Token-ABC")
        got = api.get(id=652)

        self.assertEqual(got['id'], 652)
        self.assertEqual(len(got['tags']), 2)

    @responses.activate
    def test_link_create(self):
        with open('tests/fixtures/api/links_get_one.json') as fixture:
            responses.add(responses.POST, 'http://example.com/api/v1/links',
                          json=json.load(fixture), status=200)
        api = Links("http://example.com/api/v1/", "Token-ABC")

        link = {
            "url": "https://www.facebook.com/",
            "title": "(1) Facebook",
            "description": "Example description",
            "is_private": False,
            "check_disabled": False,
            "tags": "bookmarks,other"
        }
        got = api.create(link)
        self.assertEqual(got['id'], 652)
        self.assertEqual(len(got['tags']), 2)

    @responses.activate
    def test_link_delete(self):
        with open('tests/fixtures/api/links_delete.json') as fixture:
            responses.add(responses.DELETE, 'http://example.com/api/v1/links/123',
                          json=json.load(fixture), status=200)
        api = Links("http://example.com/api/v1/", "Token-ABC")
        got = api.delete(123)

        self.assertEqual(got, {})

    # @responses.activate
    # def test_link_update(self):
    #     with open('tests/fixtures/api/links_get_one.json') as fixture:
    #         responses.add(responses.GET, 'http://example.com/api/v1/links',
    #                       json=json.load(fixture), status=200)
    #     api = Links("http://example.com/api/v1/", "Token-ABC")
    #     got = api.update()
