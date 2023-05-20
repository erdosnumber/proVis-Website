# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.companies import Companies  # noqa: E501
from swagger_server.models.company_request import CompanyRequest  # noqa: E501
from swagger_server.test import BaseTestCase


class TestCompaniesController(BaseTestCase):
    """CompaniesController integration test stubs"""

    def test_companies_get(self):
        """Test case for companies_get

        get a list of all companies
        """
        response = self.client.open(
            '/api/companies',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_companies_post(self):
        """Test case for companies_post

        create a new Company
        """
        body = {
        "about_us": "this is the best",
        "company_img_url": "url4",
        "name": "testcompany4",
        "website_link": "websitelink4"
        }
        response = self.client.open(
            '/api/companies',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_companies_queryid_get(self):
        """Test case for companies_queryid_get

        get a company by id
        """
        response = self.client.open(
            '/api/companies/{queryid}'.format(queryid=1),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
