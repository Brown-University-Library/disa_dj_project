# -*- coding: utf-8 -*-

import json, logging, pprint, secrets, uuid

import requests
from disa_app import settings_app
from disa_app.lib import view_search_results_manager
from disa_app.models import UserProfile
from django.conf import settings as project_settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import Client
from django.test import TestCase
from django.test.utils import override_settings


log = logging.getLogger(__name__)
TestCase.maxDiff = 1000


class Record_Test( TestCase ):
    """ Checks Record data-api urls. """

    def setUp(self):
        self.random_new_record_date = secrets.choice( [  # month/day/year (future TODO: make this a more-standard ISO-format like year/month/day)
            '02/02/1492', '03/03/1493', '04/04/1494', ''
            ])
        ''' Location can have 3, 2, 1, or 0 elements.
            - Position 1 will populate the form's 'Colony/State' field.
            - Position 2 will populate the form's 'Town' field.
            - Position 3 will populate the form's 'Additional location' field.'''
        self.random_new_record_location = secrets.choice( [
            [ {'id': 735, 'label': 'Massachusetts', 'value': 'Massachusetts'},
              {'id': 21, 'label': 'Boston', 'value': 'Boston'},
              {'id': 357, 'label': 'somewhere about Pumpkin-Hill', 'value': 'somewhere about Pumpkin-Hill'}],
            [ {'id': 23, 'label': 'New York', 'value': 'New York'},
              {'id': 748, 'label': 'Albany', 'value': 'Albany'} ],
            [ {'id': 630, 'label': 'Rhode Island', 'value': 'Rhode Island'} ],
            [],                                  # this is what is sent if neither of the three location-fields are not filled out
            ] )
        self.random_new_record_national_context = secrets.choice( [
            1, # British -- note: this is what is auto-sent if the field is not filled out
            2, # American
            3, # French
            4  # Spanish
            ] )
        self.random_new_record_record_type = secrets.choice( [
            {'id': 29, 'label': 'Burial Record', 'value': 'Burial Record'},
            {'id': 1, 'label': 'Baptism', 'value': 'Baptism'},
            {'id': 20, 'label': 'Petition to Assembly', 'value': 'Petition to Assembly'},
            {'id': 0, 'label': '', 'value': ''}  # this is what is sent if the field is not filled out; the form will show "Unspecified"
            ] )
        self.random_new_record_transcription_text = secrets.choice( [
            'transcription_aaa', 'transcription_bbb', 'transcription_ccc',
            ''                                   # this is what is sent if the field is not filled out
            ] )
        self.random_new_record_image_url = secrets.choice( [
            'https://foo1.com', 'https://foo2.com', 'https://foo3.com',
            None                                 # as shown below in create_new_record(), no key-value is sent if the field is not filled out
            ] )
        # self.random_put_record_text = secrets.choice( ['aaa', 'bbb', 'ccc', 'ddd'] )
        self.create_resp_statuscode = None  # updated by create_new_record()
        self.create_resp_dct = None         # updated by create_new_record()
        self.create_resp_id = None          # updated by create_new_record()
        self.delete_resp_statuscode = None  # updated by delete_new_record()
        # self.delete_resp_dct = None     # updated by delete_new_record()

    ## HELPERS ====================

    def create_new_record(self):
        """ Creates a record for tests. """
        post_url = reverse( 'data_record_url' )
        log.debug( f'post-url, ``{post_url}``' )
        payload = {
            'citation_id': 768,
            'date': self.random_new_record_date,                            # string; see self.random_new_record_date
            'locations': self.random_new_record_location,                   # list of dicts; see self.random_new_record_location
            'national_context': self.random_new_record_national_context,    # int
            'record_type': self.random_new_record_record_type,              # dict; see self.random_new_record_record_type
            'transcription': self.random_new_record_transcription_text      # string
            }
        if self.random_new_record_image_url:
            payload['image_url'] = self.random_new_record_image_url         # string; but no key-value data is sent if not filled-out
        log.debug( f'payload, ``{payload}``' )
        jsn = json.dumps( payload )
        response = self.client.post( post_url, data=jsn, content_type='application/json' )
        self.create_resp_statuscode = response.status_code
        self.post_resp_dct = json.loads( response.content )
        log.debug( f'create_new_record response dict, ``{self.post_resp_dct}``' )
        redirect_value = self.post_resp_dct['redirect']
        parts = redirect_value.split( '/' )
        self.create_resp_id = parts[-2]
        log.debug( f'create_resp_id, ``{self.create_resp_id}``' )
        # self.assertEqual( self.post_resp_id.isnumeric(), True )

    def delete_new_record(self):
        """ Deletes citation used by tests."""
        delete_url = reverse( 'data_reference_url', kwargs={'rfrnc_id': self.create_resp_id} )
        response = self.client.delete( delete_url )
        self.delete_resp_statuscode = response.status_code
        self.delete_resp_dct = json.loads( response.content )

    # ## GET LIST ===================

    # """ not applicable -- there _is_ code, but it is not used, for getting a list of citations """

    # ## GET SINGLE ===================

    # def test_get_single_bad(self):
    #     """ Checks bad GET of `http://127.0.0.1:8000/data/documents/foo`. """
    #     get_url = reverse( 'data_documents_url', kwargs={'doc_id': 'foo'} )
    #     log.debug( f'get_url, ``{get_url}``' )
    #     response = self.client.get( get_url )
    #     self.assertEqual( 404, response.status_code )
    #     self.assertEqual( b'404 / Not Found', response.content )

    # def test_get_single_good(self):
    #     """ Checks good GET of `http://127.0.0.1:8000/data/documents/abcd/`. """
    #     ## create citation
    #     self.create_new_citation()
    #     ## GET
    #     get_url = reverse( 'data_documents_url', kwargs={'doc_id': self.post_resp_id} )
    #     log.debug( f'get_url, ``{get_url}``' )
    #     response = self.client.get( get_url )
    #     log.debug( f'response.content, ``{response.content}``' )
    #     ## tests
    #     self.assertEqual( 200, response.status_code )
    #     resp_dct = json.loads( response.content )
    #     self.assertEqual(
    #         ['doc', 'doc_types'],
    #         sorted(resp_dct.keys()) )
    #     doc_keys = sorted( resp_dct['doc'].keys() )
    #     self.assertEqual(
    #         ['acknowledgements', 'citation', 'citation_type_id', 'comments', 'fields', 'id'],
    #         doc_keys )
    #     self.assertEqual(
    #         f'acks--{self.random_new_citation_text}', resp_dct['doc']['acknowledgements']
    #         )
    #     self.assertEqual(
    #         f'title--{self.random_new_citation_text}', resp_dct['doc']['citation']
    #         )  # note, the display will be some combination of the `fields` data sent
    #     self.assertEqual(
    #         f'comments--{self.random_new_citation_text}', resp_dct['doc']['comments']
    #         )
    #     self.assertEqual(
    #         {'title': f'title--{self.random_new_citation_text}'},
    #         resp_dct['doc']['fields']
    #         )
    #     ## cleanup
    #     self.delete_new_citation()

    # ## CREATE ====================

    # def test_post_bad(self):
    #     """ Checks `http://127.0.0.1:8000/data/records/` POST w/bad params. """
    #     post_url = reverse( 'data_record_url' )
    #     log.debug( f'post-url, ``{post_url}``' )
    #     payload = {
    #         'foo': 'bar'
    #     }
    #     response = self.client.post( post_url, payload )
    #     log.debug( f'create_new_record response (bytes), ``{response.content}``' )
    #     self.assertEqual( 400, response.status_code )
    #     self.assertEqual( b'400 / Bad Request', response.content )

    def test_post_good(self):
        """ Checks `http://127.0.0.1:8000/data/records/` POST w/good params. """
        ## create record
        self.create_new_record()
        ## tests
        self.assertEqual( 200, self.create_resp_statuscode )
        self.assertEqual( True, self.create_resp_id.isnumeric(),  )
        self.assertEqual( str, type(self.create_resp_id) )
        self.assertEqual( ['redirect'], list(self.post_resp_dct.keys()) )
        ## cleanup
        # self.delete_new_record()

    # ## UPDATE ====================

    # def test_put_bad(self):
    #     """ Checks bad PUT to `http://127.0.0.1:8000/data/documents/foo/`. """
    #     put_url = reverse( 'data_documents_url', kwargs={'doc_id': 'foo'} )
    #     put_response = self.client.put( put_url )
    #     self.assertEqual( 400, put_response.status_code )
    #     self.assertTrue( b'Bad Request' in put_response.content )

    # def test_put_good(self):
    #     """ Checks good PUT to `http://127.0.0.1:8000/data/documents/abcd/`. """
    #     ## create citation
    #     self.create_new_citation()
    #     ## PUT
    #     put_url = reverse( 'data_documents_url', kwargs={'doc_id': self.post_resp_id} )
    #     log.debug( f'put_url-url, ``{put_url}``' )
    #     put_payload = {  # same as create, except for `shortTitle`, which was blank
    #         'acknowledgements': f'acks--{self.random_new_citation_text}',
    #         'citation_type_id': 20,  # means the fields below will be 'Book' fields
    #         'comments': f'comments--{self.random_new_citation_text}',
    #         'fields': {
    #             'ISBN': '',
    #             'abstractNote': '',
    #             'accessDate': '',
    #             'archive': '',
    #             'archiveLocation': '',
    #             'author': '',
    #             'callNumber': '',
    #             'date': '',
    #             'edition': '',
    #             'extra': '',
    #             'language': '',
    #             'libraryCatalog': '',
    #             'numPages': '',
    #             'numberOfVolumes': '',
    #             'pages': '',
    #             'place': '',
    #             'publisher': '',
    #             'rights': '',
    #             'series': '',
    #             'seriesNumber': '',
    #             'shortTitle': f'shortTitle--{self.random_put_citation_text}',  # <-- this is the only change
    #             'title': f'title--{self.random_new_citation_text}',
    #             'url': '',
    #             'volume': ''}
    #         }
    #     jsn = json.dumps( put_payload )
    #     put_response = self.client.put( put_url, data=jsn, content_type='application/json' )
    #     put_resp_dct = json.loads( put_response.content )
    #     log.debug( f'put_resp_dct, ``{pprint.pformat(put_resp_dct)}``' )
    #     ## tests
    #     ''' Note, they're similar the 'get' tests, with two differences:
    #         1) no `fields` are returned in the PUT response;
    #         2) the 'citation' (title) check: it now incorporates (additionally) the _updated_ `shortTitle`
    #     '''
    #     self.assertEqual( 200, put_response.status_code )
    #     self.assertEqual(
    #         ['doc', 'doc_types'],
    #         sorted(put_resp_dct.keys()) )
    #     doc_keys = sorted( put_resp_dct['doc'].keys() )
    #     log.debug( f'doc_keys, ``{doc_keys}``' )
    #     self.assertEqual( # same as `create` test
    #         f'acks--{self.random_new_citation_text}',
    #         put_resp_dct['doc']['acknowledgements']
    #         )
    #     self.assertEqual( # same as `create` test
    #         f'comments--{self.random_new_citation_text}',
    #         put_resp_dct['doc']['comments']
    #         )
    #     self.assertEqual(
    #         ['acknowledgements', 'citation', 'citation_type_id', 'comments', 'id'],  # no `fields`, as in the `create` response-dct
    #         doc_keys
    #         )
    #     self.assertEqual(
    #         'title--%s, shortTitle--%s' % ( self.random_new_citation_text, self.random_put_citation_text ),
    #         put_resp_dct['doc']['citation']
    #         )  # note, the display _was_ just the contents of fields['title'], but is now the contents of that, plus fields['shortTitle']
    #     ## cleanup
    #     self.delete_new_citation()

    # ## DELETE ====================

    # def test_delete_bad(self):
    #     """ Checks bad DELETE of `http://127.0.0.1:8000/data/reference/foo/`. """
    #     ## DELETE
    #     self.post_resp_id == 'foo'
    #     self.delete_new_record()  # will attempt to delete record-id `foo`
    #     ## tests
    #     self.assertEqual( 500, self.delete_resp_statuscode )
    #     self.assertEqual( b'500 / Server Error', self.delete_resp_content )

    def test_delete_good(self):
        """ Checks good DELETE of `http://127.0.0.1:8000/data/reference/abcd/`.
            Note that, for no good reason, this root url is _different_ from the normal `http://127.0.0.1:8000/data/records/abcd/` """
        ## create record
        self.create_new_record()
        ## DELETE
        self.delete_new_record()
        ## tests
        self.assertEqual( 200, self.delete_resp_statuscode )
        self.assertEqual(
            {'redirect': '/editor/documents/768/'},
            self.delete_resp_dct )  # for now, we're hard-coding new adds to citation-document #768

    ## end Record_Test()
