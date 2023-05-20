# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.categories import Categories  # noqa: E501
from swagger_server.test import BaseTestCase


class TestCategoriesController(BaseTestCase):
    """CategoriesController integration test stubs"""

    def test_categories_get(self):
        """Test case for categories_get

        get a list of all categories
        """
        response = self.client.open(
            '/api/categories',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
