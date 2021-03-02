# -*- coding: utf-8 -*-

import json, logging, pprint, uuid

import requests
from disa_app import settings_app
from disa_app.lib import view_search_results_manager
from disa_app.models import UserProfile
from django.conf import settings as project_settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import Client
from django.test import TestCase  # from django.test import SimpleTestCase as TestCase    ## TestCase requires db, so if you're not using a db, and want tests, try this
from django.test.utils import override_settings


log = logging.getLogger(__name__)
TestCase.maxDiff = 1000


# class ReferenceGroup_Test( TestCase ):
#     """ Checks reference-group api urls. """

#     def test_post(self):
#         """ Checks `http://127.0.0.1:8000/data/reference_group/abcd/ """
#         response = self.client.post( f'/data/reference_group/new/' )
#         payload = {
#             'count': 7,
#             'count_estimated': True,
#             'description': 'the description',
#             'reference_id': 49
#         }
#         response = self.client.post( reverse('data_group_url'), payload=payload )
#         self.assertEqual( 200, response.status_code )
#         resp_dct = json.loads( response.content )
#         self.assertEqual( ['foo'], sorted(resp_dct.keys()) )


class Client_ReferenceGroup_Test( TestCase ):
    """ Checks reference-group api urls. """

    def test_post_bad(self):
        """ Checks `http://127.0.0.1:8000/data/reference_group/abcd/ w/bad params. """
        post_url = reverse( 'data_group_url', kwargs={'incoming_uuid': 'new'} )
        log.debug( f'post-url, ``{post_url}``' )
        payload = {
            'foo': 'bar'
        }
        response = self.client.post( post_url, payload )
        self.assertEqual( 400, response.status_code )
        self.assertTrue( b'Bad Request' in response.content )

    def test_post_good(self):
        """ Checks `http://127.0.0.1:8000/data/reference_group/abcd/ w/good params. """
        post_url = reverse( 'data_group_url', kwargs={'incoming_uuid': 'new'} )
        log.debug( f'post-url, ``{post_url}``' )
        payload = {
            'count': 7,
            'count_estimated': True,
            'description': 'the description',
            'reference_id': 49
        }
        response = self.client.post( post_url, payload )
        self.assertEqual( 200, response.status_code )
        resp_dct = json.loads( response.content )
        self.assertEqual( ['foo'], sorted(resp_dct.keys()) )

    # def test_get_record_data(self):
    #     """ Checks `http://127.0.0.1:8000/data/records/49/ """
    #     response = self.client.get( '/data/records/49/' )
    #     self.assertEqual( 200, response.status_code )
    #     resp_dct = json.loads( response.content )
    #     self.assertEqual( ['entrants', 'groups', 'rec'], sorted(resp_dct.keys()) )
    #     # group_keys = resp_dct['groups'][0].keys()
    #     # self.assertEqual( ['foo'], sorted(group_keys) )

    ## end Client_ReferenceGroup_Test()


class Client_Misc_Test( TestCase ):
    """ Checks miscellaneous url responses. """

    def test_browse_url(self):
        """ Checks '/browse/'. """
        response = self.client.get( '/browse/' )  # project root part of url is assumed
        self.assertEqual( 200, response.status_code )  # login landing page
        self.assertEqual( True, b'login' in response.content )

    def test_root_url_no_slash(self):
        """ Checks '/root_url' (with no slash). """
        response = self.client.get( '' )  # project root part of url is assumed
        self.assertEqual( 302, response.status_code )  # permanent redirect
        redirect_url = response._headers['location'][1]
        self.assertEqual(  '/info/', redirect_url )

    def test_root_url_slash(self):
        """ Checks '/root_url/' (with slash). """
        response = self.client.get( '/' )  # project root part of url is assumed
        self.assertEqual( 302, response.status_code )  # permanent redirect
        redirect_url = response._headers['location'][1]
        self.assertEqual(  '/info/', redirect_url )

    @override_settings(DEBUG=True)
    def test_error_url_on_dev(self):
        """ Checks that '/error_check/' url generates an exception in development.
            Note: for tests, django sets settings.DEBUG to False, thus this override.
            Note: for tests, django will not trigger the email, so setting another terminal window to:
                  python3 -m smtpd -n -c DebuggingServer localhost:1026
                  ...will not show a sent email (it will on a localhost web-hit of the url, though)
            Thanks to B.C. and <https://stackoverflow.com/a/13596201> for figuring out how to test for an exception. """
        log.debug( f'project_settings.DEBUG, ``{project_settings.DEBUG}``' )
        result = 'init'
        try:
            response = self.client.get( '/error_check/' )
        except Exception as e:
            log.debug( f'e, ``{e}``' )
            result = repr(e)
        self.assertTrue( 'Exception' in result )  # web-hit returns standard 500 http-status
        self.assertTrue( 'error-check triggered; admin emailed' in result )

    def test_error_url_on_production(self):
        """ Checks '/error_check/' url.
            Note: for testing, django defaults settings.DEBUG to False """
        log.debug( f'project_settings.DEBUG, ``{project_settings.DEBUG}``' )
        response = self.client.get( '/error_check/' )
        self.assertEqual( 404, response.status_code )

    # end class Client_Misc_Test()


class ClientDocDataTest( TestCase ):
    """ Checks document-data url responses. """

    ## does not pass ##
    # def test_doc_get_not_logged_in(self):
    #     """ Checks GET. """
    #     response = self.client.get( '/data/documents/1/' )
    #     log.debug( f'response, ``{response}``' )
    #     log.debug( f'response.__dict__, ``{response.__dict__}``' )
    #     self.assertEqual( 302, response.status_code )  # permanent redirect
    #     redirect_url = response._headers['location'][1]
    #     self.assertEqual(  '/login/', redirect_url )

    def test_data_doc_get_logged_in(self):
        """ Checks that logged-in api-GET returns response. """
        usr = User.objects.create( username='test_user' )
        usr.set_password('test_password')
        usr.save()  # creates a UserProfile object
        client = Client()
        logged_in = client.login( username='test_user', password='test_password' )
        self.assertEqual( True, logged_in )  # but does not get past shib-decorator -- request.user.is_authenticated stays False; added host-check to shib-decorator
        response = self.client.get( '/data/documents/1/' )
        log.debug( f'response, ``{response}``' )
        log.debug( f'response.__dict__, ``{response.__dict__}``' )
        self.assertEqual( 200, response.status_code )  # not yet working -- should be 200, but redirects to login

    def test_good_doc_get_logged_in(self):
        """ Checks that logged-in docoumet-GET, for existing citation, returns response. """
        usr = User.objects.create( username='test_user' )
        usr.save()  # creates a UserProfile object
        client = Client()
        client.force_login( usr )  # does not get past shib-decorator -- request.user.is_authenticated stays False; added host-check to shib-decorator
        response = self.client.get( '/editor/documents/1/' )
        self.assertEqual( 200, response.status_code )  # not yet working -- should be 200, but redirects to login

    def test_good_doc_get_logged_in(self):
        """ Checks that logged-in docoumet-GET, for existing citation, returns response. """
        usr = User.objects.create( username='test_user' )
        usr.save()  # creates a UserProfile object
        client = Client()
        client.force_login( usr )  # does not get past shib-decorator -- request.user.is_authenticated stays False; added host-check to shib-decorator
        response = self.client.get( '/editor/documents/1/' )
        self.assertEqual( 200, response.status_code )
        self.assertTrue( b'Document...' in response.content )

    def test_not_found_doc_get_logged_in(self):
        """ Checks that logged-in docoumet-GET, for non-existent citation, returns 404. """
        usr = User.objects.create( username='test_user' )
        usr.save()  # creates a UserProfile object
        client = Client()
        client.force_login( usr )  # does not get past shib-decorator -- request.user.is_authenticated stays False; added host-check to shib-decorator
        response = self.client.get( '/editor/documents/99999/' )
        self.assertEqual( 404, response.status_code )




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
