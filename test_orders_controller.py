# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.order_request import OrderRequest  # noqa: E501
from swagger_server.models.orders import Orders  # noqa: E501
from swagger_server.test import BaseTestCase


class TestOrdersController(BaseTestCase):
    """OrdersController integration test stubs"""

    def test_get_customer_order(self):
        """Test case for get_customer_order

        get a customer's specific order by id of both
        """
        response = self.client.open(
            '/api/customers/{queryid}/orders/{orderid}'.format(queryid=1, orderid=1),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_customer_orders(self):
        """Test case for get_customer_orders

        get a list of all orders of a specific customers
        """
        response = self.client.open(
            '/api/customers/{queryid}/orders'.format(queryid=1),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_order(self):
        """Test case for post_order

        create a new order for a customer with given id
        """
        body = {
        "cus_uid": "1",
        "message": "string",
        "order_date_time": "2023-04-28T17:26:48.283Z",
        "p_uid": "1"
        }
        response = self.client.open(
            '/api/customers/{queryid}/orders'.format(queryid=1),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
