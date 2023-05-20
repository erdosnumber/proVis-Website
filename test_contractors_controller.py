# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.contractor_request import ContractorRequest  # noqa: E501
from swagger_server.models.contractors import Contractors  # noqa: E501
from swagger_server.test import BaseTestCase


class TestContractorsController(BaseTestCase):
    """ContractorsController integration test stubs"""

    def test_get_contractor(self):
        """Test case for get_contractor

        get a contractor by id
        """
        response = self.client.open(
            '/api/contractors/{queryid}'.format(queryid=1),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_contractors(self):
        """Test case for get_contractors

        get a list of all contractors
        """
        response = self.client.open(
            '/api/contractors',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_contractor(self):
        """Test case for post_contractor

        create a new contractor
        """
        body = {
        "address": "address4",
        "company_id": "1",
        "email": "testemail4",
        "name": "testcontractor4",
        "phone_no": 123
        }
        response = self.client.open(
            '/api/contractors',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
