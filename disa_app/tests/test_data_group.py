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
from django.test import TestCase  # from django.test import SimpleTestCase as TestCase    ## TestCase requires db, so if you're not using a db, and want tests, try this
from django.test.utils import override_settings


log = logging.getLogger(__name__)
TestCase.maxDiff = 1000


class Client_ReferenceGroup_Test( TestCase ):
    """ Checks reference-group api urls. """

    ## GET =======================

    def test_get_bad(self):
        """ Checks bad GET of `http://127.0.0.1:8000/data/reference_group/abcd/`. """
        get_url = reverse( 'data_group_url', kwargs={'incoming_uuid': 'foo'} )
        log.debug( f'get_url, ``{get_url}``' )
        response = self.client.get( get_url )
        self.assertEqual( 404, response.status_code )
        self.assertTrue( b'Not Found' in response.content )

    def test_get_good(self):
        """ Checks good GET of `http://127.0.0.1:8000/data/reference_group/abcd/`. """
        get_url = reverse( 'data_group_url', kwargs={'incoming_uuid': '55062fa7c60f4ff9be2698b68ea9da8a'} )
        log.debug( f'get_url, ``{get_url}``' )
        response = self.client.get( get_url )
        self.assertEqual( 200, response.status_code )
        resp_dct = json.loads( response.content )
        self.assertEqual( ['request', 'response'], sorted(resp_dct.keys()) )
        req_keys = sorted( resp_dct['request'].keys() )
        self.assertEqual( ['method', 'payload', 'timestamp', 'url'], req_keys )
        resp_keys = sorted( resp_dct['response'].keys() )
        self.assertEqual( ['elapsed_time', 'group_data'], resp_keys )
        resp_group_data_keys = sorted( resp_dct['response']['group_data'].keys() )
        self.assertEqual( ['count', 'count_estimated', 'date_created', 'date_modified', 'description', 'reference_id', 'uuid' ], resp_group_data_keys )

    ## CREATE ====================

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

    # def test_post_good(self):
    #     """ Checks `http://127.0.0.1:8000/data/reference_group/abcd/ w/good params. """
    #     post_url = reverse( 'data_group_url', kwargs={'incoming_uuid': 'new'} )
    #     log.debug( f'post-url, ``{post_url}``' )
    #     payload = {
    #         'count': 7,
    #         'count_estimated': True,
    #         'description': 'the description',
    #         'reference_id': 49
    #     }
    #     response = self.client.post( post_url, payload )
    #     self.assertEqual( 200, response.status_code )
    #     resp_dct = json.loads( response.content )
    #     self.assertEqual( ['request', 'response'], sorted(resp_dct.keys()) )
    #     req_keys = sorted( resp_dct['request'].keys() )
    #     self.assertEqual( ['method', 'payload', 'timestamp', 'url'], req_keys )
    #     req_payload_keys = sorted( resp_dct['request']['payload'].keys() )
    #     self.assertEqual( ['count', 'count_estimated', 'description', 'reference_id'], req_payload_keys )
    #     resp_keys = sorted( resp_dct['response'].keys() )
    #     self.assertEqual( ['elapsed_time', 'group_data'], resp_keys )
    #     resp_group_data_keys = sorted( resp_dct['response']['group_data'].keys() )
    #     self.assertEqual( ['count', 'count_estimated', 'date_created', 'date_modified', 'description', 'reference_id', 'uuid' ], resp_group_data_keys )

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
        # response = self.client.post( post_url, payload )

        jsn = json.dumps( payload )
        response = self.client.post( post_url, data=jsn,  content_type='application/json' )


        self.assertEqual( 200, response.status_code )
        resp_dct = json.loads( response.content )
        self.assertEqual( ['request', 'response'], sorted(resp_dct.keys()) )
        req_keys = sorted( resp_dct['request'].keys() )
        self.assertEqual( ['method', 'payload', 'timestamp', 'url'], req_keys )
        req_payload_keys = sorted( resp_dct['request']['payload'].keys() )
        self.assertEqual( ['count', 'count_estimated', 'description', 'reference_id'], req_payload_keys )
        resp_keys = sorted( resp_dct['response'].keys() )
        self.assertEqual( ['elapsed_time', 'group_data'], resp_keys )
        resp_group_data_keys = sorted( resp_dct['response']['group_data'].keys() )
        self.assertEqual( ['count', 'count_estimated', 'date_created', 'date_modified', 'description', 'reference_id', 'uuid' ], resp_group_data_keys )

    ## UPDATE ====================

    def test_put_bad(self):
        """ Checks bad PUT of `http://127.0.0.1:8000/data/reference_group/abcd/`. """
        put_url = reverse( 'data_group_url', kwargs={'incoming_uuid': 'foo'} )
        put_response = self.client.put( put_url )
        self.assertEqual( 400, put_response.status_code )
        self.assertTrue( b'Bad Request' in put_response.content )

    def test_put_good(self):
        """ Checks good PUT of `http://127.0.0.1:8000/data/reference_group/abcd/`. """
        uuid = 'e2be12a88dc2455dbb0aaaab84828dc8'
        self.assertEqual( str, type(uuid) )
        ## put -> put ===========================
        put_url = reverse( 'data_group_url', kwargs={'incoming_uuid': uuid} )
        log.debug( f'put_url-url, ``{put_url}``' )
        possible_counts = [ 2, 4, 6, 8, 10 ]
        possible_descriptions = [ 'fooA', 'fooB', 'fooC', 'fooD', 'fooE' ]
        put_payload = {
            'count': secrets.choice( possible_counts ),
            'count_estimated': False,
            'description': secrets.choice( possible_descriptions ),
            'reference_id': 49
        }
        jsn = json.dumps( put_payload )
        put_response = self.client.put( put_url, data=jsn )
        put_resp_dct = json.loads( put_response.content )
        self.assertEqual( 200, put_response.status_code )
        resp_dct = json.loads( put_response.content )
        self.assertEqual( ['request', 'response'], sorted(resp_dct.keys()) )
        req_keys = sorted( resp_dct['request'].keys() )
        self.assertEqual( ['method', 'payload', 'timestamp', 'url'], req_keys )
        req_payload_keys = sorted( resp_dct['request']['payload'].keys() )
        self.assertEqual( ['count', 'count_estimated', 'description', 'reference_id'], req_payload_keys )
        resp_keys = sorted( resp_dct['response'].keys() )
        self.assertEqual( ['elapsed_time', 'group_data'], resp_keys )
        resp_group_data_keys = sorted( resp_dct['response']['group_data'].keys() )
        self.assertEqual( ['count', 'count_estimated', 'date_created', 'date_modified', 'description', 'reference_id', 'uuid' ], resp_group_data_keys )

    # def test_put_good(self):
    #     """ Checks good PUT of `http://127.0.0.1:8000/data/reference_group/abcd/`. """
    #     ## put -> create entry ==================
    #     post_url = reverse( 'data_group_url', kwargs={'incoming_uuid': 'new'} )
    #     log.debug( f'post-url, ``{post_url}``' )
    #     post_payload = {
    #         'count': 7,
    #         'count_estimated': True,
    #         'description': 'the description',
    #         'reference_id': 49
    #     }
    #     post_response = self.client.post( post_url, post_payload )
    #     post_resp_dct = json.loads( post_response.content )
    #     new_uuid = post_resp_dct['response']['group_data']['uuid']
    #     self.assertEqual( str, type(new_uuid) )
    #     ## put -> put ===========================
    #     put_url = reverse( 'data_group_url', kwargs={'incoming_uuid': new_uuid} )
    #     log.debug( f'put_url-url, ``{put_url}``' )
    #     put_payload = {
    #         'count': 8,
    #         'count_estimated': False,
    #         'description': 'the new description',
    #         'reference_id': 49
    #     }
    #     jsn = json.dumps( put_payload )
    #     put_response = self.client.put( put_url, data=jsn )
    #     put_resp_dct = json.loads( put_response.content )
    #     self.assertEqual( 200, put_response.status_code )
    #     resp_dct = json.loads( put_response.content )
    #     self.assertEqual( ['request', 'response'], sorted(resp_dct.keys()) )
    #     req_keys = sorted( resp_dct['request'].keys() )
    #     self.assertEqual( ['method', 'payload', 'timestamp', 'url'], req_keys )
    #     req_payload_keys = sorted( resp_dct['request']['payload'].keys() )
    #     self.assertEqual( ['count', 'count_estimated', 'description', 'reference_id'], req_payload_keys )
    #     resp_keys = sorted( resp_dct['response'].keys() )
    #     self.assertEqual( ['elapsed_time', 'group_data'], resp_keys )
    #     resp_group_data_keys = sorted( resp_dct['response']['group_data'].keys() )
    #     self.assertEqual( ['count', 'count_estimated', 'date_created', 'date_modified', 'description', 'reference_id', 'uuid' ], resp_group_data_keys )
    #     ## put -> deletion ======================
    #     delete_url = reverse( 'data_group_url', kwargs={'incoming_uuid': new_uuid} )
    #     delete_response = self.client.delete( delete_url )
    #     self.assertEqual( 200, delete_response.status_code )
    #     resp_dct = json.loads( delete_response.content )
    #     self.assertEqual( ['request', 'response'], sorted(resp_dct.keys()) )
    #     req_keys = sorted( resp_dct['request'].keys() )
    #     self.assertEqual( ['method', 'payload', 'timestamp', 'url'], req_keys )
    #     resp_keys = sorted( resp_dct['response'].keys() )
    #     self.assertEqual( ['elapsed_time', 'status'], resp_keys )

    ## DELETE ====================

    def test_delete_bad(self):
        """ Checks bad DELETE of `http://127.0.0.1:8000/data/reference_group/abcd/`. """
        delete_url = reverse( 'data_group_url', kwargs={'incoming_uuid': 'foo'} )
        delete_response = self.client.delete( delete_url )
        self.assertEqual( 404, delete_response.status_code )
        self.assertTrue( b'Not Found' in delete_response.content )

    def test_delete_good(self):
        """ Checks good DELETE of `http://127.0.0.1:8000/data/reference_group/abcd/`. """
        ## first create entry
        post_url = reverse( 'data_group_url', kwargs={'incoming_uuid': 'new'} )
        log.debug( f'post-url, ``{post_url}``' )
        payload = {
            'count': 7,
            'count_estimated': True,
            'description': 'the description',
            'reference_id': 49
        }
        post_response = self.client.post( post_url, payload )
        post_resp_dct = json.loads( post_response.content )
        new_uuid = post_resp_dct['response']['group_data']['uuid']
        self.assertEqual( str, type(new_uuid) )
        ## deletion
        delete_url = reverse( 'data_group_url', kwargs={'incoming_uuid': new_uuid} )
        delete_response = self.client.delete( delete_url )
        self.assertEqual( 200, delete_response.status_code )
        resp_dct = json.loads( delete_response.content )
        self.assertEqual( ['request', 'response'], sorted(resp_dct.keys()) )
        req_keys = sorted( resp_dct['request'].keys() )
        self.assertEqual( ['method', 'payload', 'timestamp', 'url'], req_keys )
        resp_keys = sorted( resp_dct['response'].keys() )
        self.assertEqual( ['elapsed_time', 'status'], resp_keys )

    ## RECORD-GET ================

    def test_get_record_data_for_group_check(self):
        """ Checks `http://127.0.0.1:8000/data/records/49/ """
        response = self.client.get( '/data/records/49/' )
        self.assertEqual( 200, response.status_code )
        resp_dct = json.loads( response.content )
        self.assertEqual( ['entrants', 'groups', 'rec'], sorted(resp_dct.keys()) )
        try:
            resp_group_data_keys = sorted( resp_dct['groups']['group_data'][0].keys() )
            self.assertEqual( ['count', 'count_estimated', 'date_created', 'date_modified', 'description', 'reference_id', 'uuid' ], resp_group_data_keys )
        except:
            pass

    ## end Client_ReferenceGroup_Test()
