# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.customers import Customers  # noqa: E501
from swagger_server.models.register_response import RegisterResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestCustomersController(BaseTestCase):
    """CustomersController integration test stubs"""

    def test_get_customer(self):
        """Test case for get_customer

        get a customer by id
        """
        response = self.client.open(
            '/api/customers/{queryid}'.format(queryid=1),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_customers(self):
        """Test case for get_customers

        get a list of all customers
        """
        response = self.client.open(
            '/api/customers',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_customers(self):
        """Test case for post_customers

        create a new customer
        """
        body = {
        "emailid": "email1",
        "name": "name1",
        "password": "password",
        "phone_number": 123
        }
        response = self.client.open(
            '/api/customers',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
