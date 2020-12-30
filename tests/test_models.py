#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import unittest
from datetime import datetime, timezone

from linkace_cli import models


class TestLinkAceCLI(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_model_link(self):
        with open('tests/fixtures/models/link.json', 'r') as fixture:
            got = models.Link().load(json.load(fixture))

        self.assertEqual(got['id'], 85)
        self.assertEqual(got['user_id'], 1)
        self.assertEqual(got['created_at'], datetime(2020, 3, 9, 19, 33, 23, tzinfo=timezone.utc))

    def test_model_list(self):
        with open('tests/fixtures/models/list.json', 'r') as fixture:
            got = models.List().load(json.load(fixture))

        self.assertEqual(got['id'], 3)
        self.assertEqual(got['user_id'], 1)
        self.assertEqual(got['created_at'], datetime(2020, 1, 24, 13, 13, 2, tzinfo=timezone.utc))

    def test_model_note(self):
        with open('tests/fixtures/models/note.json', 'r') as fixture:
            got = models.Note().load(json.load(fixture))

        self.assertEqual(got['id'], 85)
        self.assertEqual(got['user_id'], 1)
        self.assertEqual(got['created_at'], datetime(2020, 3, 9, 19, 33, 23, tzinfo=timezone.utc))

    def test_model_tag(self):
        with open('tests/fixtures/models/tag.json', 'r') as fixture:
            got = models.Tag().load(json.load(fixture))

        self.assertEqual(got['id'], 118)
        self.assertEqual(got['user_id'], 1)
        self.assertEqual(got['created_at'], datetime(2019, 2, 24, 20, 39, 25, tzinfo=timezone.utc))
