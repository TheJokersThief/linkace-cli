#!/usr/bin/env python
# -*- coding: utf-8 -*-
import responses
import unittest

from linkace_cli.api import LinkAceHTTPSession, LinkAce


class TestLinkAceCLI(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_http_session_headers(self):
        got = LinkAceHTTPSession('http://example.com/api', 'Token-ABCDEFGHJ')
        wanted = {
            'User-Agent': 'Linkace-CLI',
            'Accept-Encoding': 'gzip, deflate',
            'Accept': 'application/json',
            'Connection': 'keep-alive',
            'Authorization': 'Bearer Token-ABCDEFGHJ'
        }

        self.assertEqual(got.headers, wanted)

    @responses.activate
    def test_http(self, *args):
        # GET request
        responses.add(responses.GET, 'http://example.com/api',
                      json={}, status=200)
        http = LinkAce('http://example.com/api', 'Token-ABCDEFGHJ')
        resp = http.get("")

        self.assertEqual(resp, {})

        # POST request
        responses.add(responses.POST, 'http://example.com/api',
                      json={}, status=200)
        http = LinkAce('http://example.com/api', 'Token-ABCDEFGHJ')
        resp = http.post("")

        self.assertEqual(resp, {})
