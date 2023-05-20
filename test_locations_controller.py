# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.locations import Locations  # noqa: E501
from swagger_server.test import BaseTestCase


class TestLocationsController(BaseTestCase):
    """LocationsController integration test stubs"""

    def test_locations_get(self):
        """Test case for locations_get

        get a list of all locations
        """
        response = self.client.open(
            '/api/locations',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
