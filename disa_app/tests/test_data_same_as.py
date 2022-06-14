""" Tests the Referent-Match API. 

Documentation...

Notes
- All data API endpoints assume authentication.
- Re 'confidence' shown in response and some payloads: it's experimental; not used; will very likely be replaced with ``predicate: is_same_as``.
- PUT for now only allows modification of notes, so for clarity, that's all the payload shows.
  (http PUT spec implies full payload replaces all existing data -- functionally this is a PATCH).
- All payloads shown as dicts for convenience; they should be sent as json byte-strings.
- Responses shown as dicts, for convenience, are actually json byte-strings.

## create -----------------------------------------------------------

url... 
<http://127.0.0.1/data/referent_match/new/>

payload (dict shown, but sent as json)...
{
    'confidence': 100,  # experimental; not used; will likely be replaced with ``predicate: is_same_as``
    'researcher_notes': 'the notes',
    'rfrnt_obj_uuid': 'f30cc74cb2014a5b9d98d0aa45ea4b3e',
    'rfrnt_sbj_uuid': '9d937d545ec943a3b5e436868dc0a2ce'
}

response...
{'request': {'method': 'POST',
             'payload': {'confidence': 100,
                         'researcher_notes': 'the notes',
                         'rfrnt_obj_uuid': 'fa9a027d152d43d394831d3a88757519',
                         'rfrnt_sbj_uuid': '12a3012c1ffc4d0b90ad3b8cd1e4229c'},
             'timestamp': '2022-06-14 06:01:36.726913',
             'url': 'http://127.0.0.1/data/referent_match/new/'},
 'response': {'elapsed_time': '0:00:00.004249',
              'referent_match_data': {'confidence': 100,
                                      'date_created': '2022-06-14 '
                                                      '06:01:36.728822',
                                      'date_edited': '2022-06-14 '
                                                     '06:01:36.728824',
                                      'referent_obj_uuid': 'fa9a027d152d43d394831d3a88757519',
                                      'referent_sbj_uuid': '12a3012c1ffc4d0b90ad3b8cd1e4229c',
                                      'researcher_notes': 'the notes',
                                      'uuid': 'a0f5c69ec0d84ea39e08b1f1a806ba4d'}}}

## read -------------------------------------------------------------

url...
<http://127.0.0.1/data/referent_match/a0f5c69ec0d84ea39e08b1f1a806ba4d/>

payload...
N/A

response...
{'request': {'method': 'GET',
             'timestamp': '2022-06-14 06:01:36.732193',
             'url': 'http://127.0.0.1/data/referent_match/a0f5c69ec0d84ea39e08b1f1a806ba4d/'},
 'response': {'elapsed_time': '0:00:00.001842',
              'referent_match_data': {'confidence': 100,
                                      'date_created': '2022-06-14 06:01:36.728822',
                                      'date_edited': '2022-06-14 06:01:36.728824',
                                      'referent_obj_uuid': 'fa9a027d152d43d394831d3a88757519',
                                      'referent_sbj_uuid': '12a3012c1ffc4d0b90ad3b8cd1e4229c',
                                      'researcher_notes': 'the notes',
                                      'uuid': 'a0f5c69ec0d84ea39e08b1f1a806ba4d'}}}

## update -----------------------------------------------------------

url...
<http://127.0.0.1/data/referent_match/7a0a05c091c54564981fec37a97a503d/>

payload (dict shown, but sent as json)...
{ 'researcher_notes': 'updated notes' }

response...
{'request': {'method': 'PUT',
             'payload': {'researcher_notes': 'updated notes'},             
             'timestamp': '2022-06-14 06:08:35.834779',
             'url': 'http://127.0.0.1/data/referent_match/7a0a05c091c54564981fec37a97a503d/'},
 'response': {'elapsed_time': '0:00:00.003936',
              'referent_match_data': {'confidence': 100,
                                      'date_created': '2022-06-13 09:08:35.831508',
                                      'date_edited': '2022-06-14 06:08:35.836694',
                                      'referent_obj_uuid': '23d1acc16a2f48e693e3676c212ee4e3',
                                      'referent_sbj_uuid': '3c0a074b9ec24207b36f9c70eaa2890f',
                                      'researcher_notes': 'updated notes',
                                      'uuid': '7a0a05c091c54564981fec37a97a503d'}}}

## delete -----------------------------------------------------------

url...
<http://127.0.0.1/data/referent_match/7a0a05c091c54564981fec37a97a503d/>

payload...
N/A

response...
b'200 / OK'
"""

import json, logging, pprint, random, uuid

from django.conf import settings as project_settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseServerError
from django.test import TestCase  # TestCase requires db, so if no db is needed, try ``from django.test import SimpleTestCase as TestCase``

log = logging.getLogger(__name__)


class Client_ReferentMatch_API_Test( TestCase ):
    """ Checks `/referent_match/1234/` api urls. """

    def setUp(self):
        self.new_subj_rfrnt_uuid: str = ''
        self.new_obj_rfrnt_uuid: str = ''
        self.new_uuid: str = ''
        self.post_resp_dct: dict = {}
        if '127.0.0.1' not in project_settings.ALLOWED_HOSTS and 'localhost' not in project_settings.ALLOWED_HOSTS:
            raise Exception( 'Not running test, because for now, it will create data in the real database.' )

    ## CREATE (post) ============================

    def test_post_good(self):
        """ Checks that good POST TO `http://127.0.0.1:8000/data/referent_match/new/`...
            ...should succeed. """
        ## create referent_match ----------------
        django_http_response = self.create_referent_match_via_post()
        ## tests --------------------------------
        self.assertEqual( 200, django_http_response.status_code )
        post_resp_dct: dict = json.loads( django_http_response.content )  # type: ignore
        self.post_resp_dct = post_resp_dct
        ## test post-response main keys
        self.assertEqual( ['request', 'response'], sorted(self.post_resp_dct.keys()) )
        ## test indicated sent payload
        req_keys = sorted( self.post_resp_dct['request'].keys() )
        self.assertEqual( ['method', 'payload', 'timestamp', 'url'], req_keys )
        ## test post-response "response" keys
        rsp_keys: list = sorted( self.post_resp_dct['response'].keys() )
        self.assertEqual( ['elapsed_time', 'referent_match_data'], rsp_keys )
        ## test post-response relationship keys
        new_relationship_keys = sorted( self.post_resp_dct['response']['referent_match_data'].keys() )
        self.assertEqual( [
            'confidence',
            'date_created',
            'date_edited',
            'referent_obj_uuid',
            'referent_sbj_uuid',
            'researcher_notes', 
            'uuid'], new_relationship_keys )
        ## cleanup ------------------------------
        relationship_uuid = self.post_resp_dct['response']['referent_match_data']['uuid']
        self.delete_referent_match_via_delete( relationship_uuid )
        return

    def test_post_relationship_already_exists(self):
        """ Checks that already-existing-relationship POST TO `http://127.0.0.1:8000/data/referent_match/new/`... 
            ...should fail with a `400 / Bad Request` """
        ## create referent-match ------------------------------------
        django_http_response = self.create_referent_match_via_post()
        self.assertEqual( 200, django_http_response.status_code )
        post_resp_dct: dict = json.loads( django_http_response.content )  # type: ignore
        self.post_resp_dct = post_resp_dct
        log.debug( f'good-creation response-dict, ``{pprint.pformat(self.post_resp_dct)}``' )
        ## try duplicate referent-match -----------------------------
        log.debug( f'about to try a duplicate referent-match')
        existing_sbj_uuid = self.post_resp_dct['response']['referent_match_data']['referent_sbj_uuid']
        log.debug( f'existing_sbj_uuid, ``{existing_sbj_uuid}``' )
        existing_obj_uuid = self.post_resp_dct['response']['referent_match_data']['referent_obj_uuid']
        log.debug( f'existing_obj_uuid, ``{existing_obj_uuid}``' )
        django_http_response_2  = self.create_referent_match_via_post( incoming_sbj_uuid=existing_sbj_uuid, incoming_obj_uuid=existing_obj_uuid )
        self.assertEqual( 400, django_http_response_2.status_code )
        ## try duplicate referent-match reversed --------------------
        django_http_response_3  = self.create_referent_match_via_post( incoming_sbj_uuid=existing_obj_uuid, incoming_obj_uuid=existing_sbj_uuid )
        self.assertEqual( 400, django_http_response_3.status_code )
        ## cleanup
        relationship_uuid = self.post_resp_dct['response']['referent_match_data']['uuid']
        self.delete_referent_match_via_delete( relationship_uuid )

    def test_post_relationship_existing_referent_to_new_referent(self):
        """ Checks that already-existing-referent--to--new-referent POST TO `http://127.0.0.1:8000/data/referent_match/new/`... 
            ...should succeed """
        ## create referent-match ------------------------------------
        django_http_response = self.create_referent_match_via_post()
        self.assertEqual( 200, django_http_response.status_code )
        post_resp_dct: dict = json.loads( django_http_response.content )  # type: ignore
        self.post_resp_dct = post_resp_dct
        log.debug( f'good-creation response-dict, ``{pprint.pformat(self.post_resp_dct)}``' )
        existing_sbj_uuid = self.post_resp_dct['response']['referent_match_data']['referent_sbj_uuid']
        ## create 3rd referent --------------------------------------
        third_rfrnt_uuid: str = self.create_new_referent()
        ## create new referent-match with 3rd referent --------------
        django_http_response_2 = self.create_referent_match_via_post( incoming_sbj_uuid=existing_sbj_uuid, incoming_obj_uuid=third_rfrnt_uuid )
        ## confirm it worked ----------------------------------------
        self.assertEqual( 200, django_http_response_2.status_code )
        ## TODO: clean up extra relationship

## TODO -- for GET-tests, do this and confirm  querying a rfrnt-uuid returns both matches

    ## READ (get) ===============================
    """ Interesting issue... 
        Should the GET be for the relationship-uuid? 
        For a referent-uuid? 
        Should it handle both?
        Or should a minimal referent-API GET call return one or more relationship-UUIDs, and then one would call...
          ...the referent_match-API to get more info about that relationshp?
    """

    def test_get_good(self):
        """ Checks good GET of: 
            `http://127.0.0.1:8000/data/referent_match/abcd.../` should succeed. """
        ## create referent_match ----------------
        django_post_response = self.create_referent_match_via_post()
        post_resp_dct: dict = json.loads( django_post_response.content )  # type: ignore
        relationship_uuid = post_resp_dct['response']['referent_match_data']['uuid']
        ## call GET api -------------------------
        url = reverse( 'data_referent_match_url', kwargs={'incoming_identifier': relationship_uuid} )  # eg `http://127.0.0.1:8000/data/referent_match/abcd.../`
        django_get_response = self.client.get( url )
        # assert type(django_get_response) in [ HttpResponse, HttpResponseServerError ] 
        # assert type(django_get_response) == HttpResponse 
        ## tests --------------------------------
        self.assertEqual( type(django_get_response), HttpResponse )
        self.assertEqual( 200, django_get_response.status_code )
        created_sbj_uuid = post_resp_dct['response']['referent_match_data']['referent_sbj_uuid']
        created_obj_uuid = post_resp_dct['response']['referent_match_data']['referent_obj_uuid']
        get_resp_dct: dict = json.loads( django_get_response.content )  # type: ignore
        self.assertEqual( created_sbj_uuid, get_resp_dct['response']['referent_match_data']['referent_sbj_uuid'] )
        self.assertEqual( created_obj_uuid, get_resp_dct['response']['referent_match_data']['referent_obj_uuid'] )

    def test_get_bad_uuid(self):
        """ Checks that GET of: 
            `http://127.0.0.1:8000/data/referent_match/not_found_uuid/` should return a 400. """
        url = reverse( 'data_referent_match_url', kwargs={'incoming_identifier': 'not_found_uuid'} )  # eg `http://127.0.0.1:8000/data/referent_match/abcd.../`
        django_get_response = self.client.get( url )
        ## tests --------------------------------
        self.assertEqual( type(django_get_response), HttpResponseBadRequest )
        self.assertEqual( 400, django_get_response.status_code )

    def test_get_not_found(self):
        """ Checks that GET of: 
            `http://127.0.0.1:8000/data/referent_match/not_found_good_uuid/` should return a 404. """
        uid: str = uuid.uuid4().hex
        url = reverse( 'data_referent_match_url', kwargs={'incoming_identifier': uid} )  # eg `http://127.0.0.1:8000/data/referent_match/abcd.../`
        django_get_response = self.client.get( url )
        ## tests --------------------------------
        self.assertEqual( type(django_get_response), HttpResponseNotFound )
        self.assertEqual( 404, django_get_response.status_code )


    ## UPDATE (put) =============================


    def test_good_put(self):
        """ Checks that PUT to: 
            `http://127.0.0.1:8000/data/referent_match/good_relationship_uuid/` should... 
            ...return a 200, and full item data. """
        ## create referent_match ----------------
        django_post_response = self.create_referent_match_via_post()
        post_resp_dct: dict = json.loads( django_post_response.content )  # type: ignore
        relationship_uuid = post_resp_dct['response']['referent_match_data']['uuid']
        ## call put-api -------------------------
        put_url = reverse( 'data_referent_match_url', kwargs={'incoming_identifier': relationship_uuid} )  # eg `http://127.0.0.1:8000/data/referent_match/abcd.../`        
        put_payload = {
            'researcher_notes': 'updated notes',
            # 'confidence': 100  # ignoring this; only allowing notes to be updated for now.
        }
        jsn = json.dumps( put_payload )
        put_response = self.client.put( put_url, data=jsn, content_type='application/json' )
        ## tests --------------------------------
        self.assertEqual( type(put_response), HttpResponse )
        self.assertEqual( 200, put_response.status_code )
        put_response_dict: dict = json.loads( put_response.content )  # type: ignore
        log.debug( f'put_response_dict, ``{pprint.pformat(put_response_dict)}``' )
        updated_notes: str = put_response_dict['response']['referent_match_data']['researcher_notes']
        self.assertEqual( 'updated notes', updated_notes )
        ## cleanup ------------------------------
        self.delete_referent_match_via_delete( relationship_uuid )


    ## DELETE ===================================

    def test_good_delete(self):
        """ Checks that a DELETE to: 
            `http://127.0.0.1:8000/data/referent_match/existing_relationship_uuid/` should... 
            ...return a 200. """
        ## create referent_match ------------------------------------
        django_post_response = self.create_referent_match_via_post()
        post_resp_dct: dict = json.loads( django_post_response.content )  # type: ignore
        relationship_uuid = post_resp_dct['response']['referent_match_data']['uuid']
        ## call delete-api ------------------------------------------
        delete_url = reverse( 'data_referent_match_url', kwargs={'incoming_identifier': relationship_uuid} )  # eg `http://127.0.0.1:8000/data/referent_match/abcd.../`        
        delete_response = self.client.delete( delete_url )
        ## tests ----------------------------------------------------
        self.assertEqual( type(delete_response), HttpResponse )
        self.assertEqual( 200, delete_response.status_code )
        self.assertEqual( b'200 / OK', delete_response.content )  # type: ignore
        ## try delete-api call a second time for 404 test -----------
        delete_response2 = self.client.delete( delete_url )
        ## tests ----------------------------------------------------
        self.assertEqual( type(delete_response2), HttpResponseNotFound )
        self.assertEqual( 404, delete_response2.status_code )
        return

    ## HELPERS ------------------------------------------------------

    def create_referent_match_via_post(self, incoming_sbj_uuid=None, incoming_obj_uuid=None ):
        """ Creates a ReferentMatch entry for tests. 
            Called by test_post_good() """
        log.debug( f'incoming_sbj_uuid, ``{incoming_sbj_uuid}``' )
        log.debug( f'incoming_obj_uuid, ``{incoming_obj_uuid}``' )
        tmp_sbj_uuid = ''
        tmp_obj_uuid = ''
        if incoming_sbj_uuid == None and incoming_obj_uuid == None:
            ## create `subject` referent
            self.new_subj_rfrnt_uuid: str = self.create_new_referent()
            log.debug( f'rfrnt_subj_uuid, ``{self.new_subj_rfrnt_uuid}``' )
            tmp_sbj_uuid = self.new_subj_rfrnt_uuid
            ## create `object` referent
            self.new_obj_rfrnt_uuid: str = self.create_new_referent()
            log.debug( f'rfrnt_obj_uuid, ``{self.new_obj_rfrnt_uuid}``' )
            tmp_obj_uuid = self.new_obj_rfrnt_uuid
        else:
            tmp_sbj_uuid = incoming_sbj_uuid
            tmp_obj_uuid = incoming_obj_uuid
        ## create referent_match entry
        post_url = reverse( 'data_referent_match_url', kwargs={'incoming_identifier': 'new'} )  # eg `http://127.0.0.1:8000/data/referent_match/new/`
        log.debug( f'post-url, ``{post_url}``' )
        payload = {
            'rfrnt_sbj_uuid': tmp_sbj_uuid,
            'rfrnt_obj_uuid': tmp_obj_uuid,
            'researcher_notes': 'the notes',
            'confidence': 100  # temporary experiment; for now always 100; explore replacing with an rdf-predicate that could be more-flexible
        }
        log.debug( f'create-referent-match-payload, ``{pprint.pformat(payload)}``' )
        jsn = json.dumps( payload )
        django_http_response = self.client.post( post_url, data=jsn, content_type='application/json' )
        return django_http_response
        ## end def create_referent_match_via_post()


    def create_new_referent(self) -> str:
        """ Creates a referent for tests; returns UUID. 
            Called by create_referent_match_via_post() """
        post_url = reverse( 'data_referent_url', kwargs={'rfrnt_id': 'new'} )
        log.debug( f'post-url, ``{post_url}``' )
        name_code = str( random.randint(1000, 9999) )
        payload = {
            'id': 'new',
            'name': {'first': f'test-first-{name_code}', 'id': 'name', 'last': f'test-last-{name_code}'},
            'record_id': '49',
            'roles': [
                {'id': '3', 'name': 'Priest'},
                {'id': '30', 'name': 'Previous Owner'}
            ]
        }
        jsn = json.dumps( payload )
        response = self.client.post( post_url, data=jsn, content_type='application/json' )
        self.assertEqual( 200, response.status_code )
        post_resp_dct: dict = json.loads( response.content )  # type: ignore
        log.debug( f'post_resp_dct, ``{pprint.pformat(post_resp_dct)}``' )
        referent_uuid: str = post_resp_dct['uuid']
        log.debug( f'referent_uuid, ``{referent_uuid}``' )
        return referent_uuid
            
    def delete_referent_match_via_delete( self, relationship_uuid: str ) -> None:
        """ Deletes new referent-match entry.
            Called by test_post_good() for now, and likely others. """
        delete_url = reverse( 'data_referent_match_url', kwargs={'incoming_identifier': relationship_uuid} )  # eg `http://127.0.0.1:8000/data/referent_match/the_uuid/`
        response = self.client.delete( delete_url )
        self.assertEqual( 200, response.status_code )
        ## see test_delete() for tests
        return

    ## end Client_ReferentMatch_API_Test()


