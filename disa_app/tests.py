# -*- coding: utf-8 -*-

import logging

from disa_app.lib import view_search_results_manager
from django.test import TestCase  # from django.test import SimpleTestCase as TestCase    ## TestCase requires db, so if you're not using a db, and want tests, try this


log = logging.getLogger(__name__)
TestCase.maxDiff = 1000


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


class SearchTest( TestCase ):
    """ Checks `view_search_results_manager` module. """

    def test_transcription_excerpt(self):
        """ Checks transcription-excertp prep for multiple cases. """
        source = """Details of advertisement: \"Ran away from Capt. John A of Boston, on Monday the 12th Currant, a tall lusty Indian Man call'd Harry, about 19 Years of Age, with a black Hat, brown Ozenbridge Breeches and Jacket: Whoever will take up said India, and bring or convey him safe either to John C Post master of Boston, or to Mr. Nathaniel N of Kingstown in Naraganset, Master to said Indian, shall have a sufficient Reward.\""""
        tests = [
            {
                'title': 'lowercase',
                'search': 'john',
                'expected': [
                    '…of advertisement: "Ran away from Capt. John A of Boston, on Monday the 12th Currant…',
                    '…and bring or convey him safe either to John C Post master of Boston, or to Mr. Nath…']
            }, {
                'title': 'uppercase',
                'search': 'John',
                'expected': [
                    '…of advertisement: "Ran away from Capt. John A of Boston, on Monday the 12th Currant…',
                    '…and bring or convey him safe either to John C Post master of Boston, or to Mr. Nath…']
            }, {
                'title': 'beginning',
                'search': 'detail',
                'expected': ['…Details of advertisement: "Ran away from Capt.…']
            }, {
                'title': 'near_end',
                'search': 'reward',
                'expected': ['…to said Indian, shall have a sufficient Reward."…']
            }, {
                'title': 'blank',
                'search': 'foo',
                'expected': []
            }
        ]
        for test in tests:
            ( title, search, expected ) = ( test['title'], test['search'], test['expected'] )
            # self.assertSequenceEqual(
            excerpt = view_search_results_manager.update_transcription( source, search )
            self.assertEqual(
                expected,
                excerpt,
                f'error on search-title, ``{title}``; excerpt, ```{excerpt}```'
                )

    # end class SearchTest()
