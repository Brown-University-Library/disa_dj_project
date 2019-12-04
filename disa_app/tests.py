# -*- coding: utf-8 -*-

import logging
from django.test import TestCase
# from django.test import SimpleTestCase as TestCase    ## TestCase requires db, so if you're not using a db, and want tests, try this


log = logging.getLogger(__name__)
TestCase.maxDiff = None


class RootUrlTest( TestCase ):
    """ Checks root urls. """

    def test_root_url_no_slash(self):
        """ Checks '/root_url' (with no slash). """
        response = self.client.get( '' )  # project root part of url is assumed
        self.assertEqual( 302, response.status_code )  # permanent redirect
        redirect_url = response._headers['location'][1]
        self.assertEqual(  '/browse/', redirect_url )

    def test_root_url_slash(self):
        """ Checks '/root_url/' (with slash). """
        response = self.client.get( '/' )  # project root part of url is assumed
        self.assertEqual( 302, response.status_code )  # permanent redirect
        redirect_url = response._headers['location'][1]
        self.assertEqual(  '/browse/', redirect_url )

    # end class RootUrlTest()
