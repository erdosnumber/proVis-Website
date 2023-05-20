# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.bookmark_request import BookmarkRequest  # noqa: E501
from swagger_server.models.bookmarks import Bookmarks  # noqa: E501
from swagger_server.test import BaseTestCase


class TestBookmarksController(BaseTestCase):
    """BookmarksController integration test stubs"""

    def test_delete_customer_bookmark(self):
        """Test case for delete_customer_bookmark
~
        deletes a specific customer's bookmark by id of both
        """
        response = self.client.open(
            '/api/customers/{queryid}/bookmarks/{bookmarkid}'.format(queryid=1, bookmarkid=29),
            method='DELETE')
        self.assertEqual(response.status_code,204)

    def test_get_customer_bookmark(self):
        """Test case for get_customer_bookmark

        get a customer's specific bookmark by id of both
        """
        response = self.client.open(
            '/api/customers/{queryid}/bookmarks/{bookmarkid}'.format(queryid=1, bookmarkid=1),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_customer_bookmarks(self):
        """Test case for get_customer_bookmarks

        get a list of all bookmarks of a specific customer
        """
        response = self.client.open(
            '/api/customers/{queryid}/bookmarks'.format(queryid=1),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_bookmark(self):
        """Test case for post_bookmark

        create a new bookmark for a customer with given id
        """
        body = {
        "cus_uid": "1",
        "p_uid": "1"
        }
        response = self.client.open(
            '/api/customers/{queryid}/bookmarks'.format(queryid='queryid_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
