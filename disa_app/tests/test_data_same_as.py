""" Tests the Referent-A is the same individual as Referent-B feature/api. """

import json, logging, pprint, random

from django.conf import settings as project_settings
from django.core.urlresolvers import reverse
from django.test import TestCase  # TestCase requires db, so if no db is needed, try ``from django.test import SimpleTestCase as TestCase``

log = logging.getLogger(__name__)


class Client_ReferentMatch_API_Test( TestCase ):
    """ Checks `/referent_match/1234/` api urls. """

    def setUp(self):
        self.new_subj_rfrnt_uuid: str = ''
        self.new_obj_rfrnt_uuid: str = ''
        self.new_uuid: str = ''
        self.post_resp_dct: dict = {}

    ## CREATE (post) ============================

    def test_post_good(self):
        """ Checks good POST TO `http://127.0.0.1:8000/data/referent_match/new/`. """
        if '127.0.0.1' not in project_settings.ALLOWED_HOSTS and 'localhost' not in project_settings.ALLOWED_HOSTS:
            raise Exception( 'Not running test, because it will create data in the real database.' )
        ## create referent_match ----------------
        self.create_referent_match_via_post()
        ## tests --------------------------------
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

    ## READ (get) ===============================

    # def test_get_good(self):
    #     """ Checks good GET of `http://127.0.0.1:8000/data/referent_match/abcd/`. """
    #     log.debug( f'allowed_hosts, ``{project_settings.ALLOWED_HOSTS}``' )
    #     if '127.0.0.1' not in project_settings.ALLOWED_HOSTS and 'localhost' not in project_settings.ALLOWED_HOSTS:
    #         raise Exception( 'Not running test, because it will create data in the real database.' )
    #     ## create referents
    #     self.new_subj_rfrnt_uuid = self.create_new_referent()
    #     self.new_obj_rfrnt_uuid = self.create_referent_match()

    #     self.assertEqual( 1, 2 )

    ## UPDATE (put) =============================

    ## DELETE ===================================

    ## HELPERS ----------------------------------

    def create_referent_match_via_post(self):
        """ Creates a ReferentMatch entry for tests. 
            Called by test_post_good() """
        ## create `subject` referent
        self.new_subj_rfrnt_uuid: str = self.create_new_referent()
        log.debug( f'rfrnt_subj_uuid, ``{self.new_subj_rfrnt_uuid}``' )
        ## create `object` referent
        self.new_obj_rfrnt_uuid: str = self.create_new_referent()
        log.debug( f'rfrnt_obj_uuid, ``{self.new_obj_rfrnt_uuid}``' )
        ## create referent_match entry
        post_url = reverse( 'data_referent_match_url', kwargs={'incoming_identifier': 'new'} )  # eg `http://127.0.0.1:8000/data/referent_match/new/`
        log.debug( f'post-url, ``{post_url}``' )
        payload = {
            'rfrnt_sbj_uuid': self.new_subj_rfrnt_uuid,
            'rfrnt_obj_uuid': self.new_obj_rfrnt_uuid,
            'researcher_notes': 'the notes',
            'confidence': 100  # temporary experiment; for now always 100; explore replacing with an rdf-predicate that could be more-flexible
        }
        log.debug( f'create-referent-match-payload, ``{pprint.pformat(payload)}``' )
        jsn = json.dumps( payload )
        response = self.client.post( post_url, data=jsn, content_type='application/json' )
        self.assertEqual( 200, response.status_code )
        self.post_resp_dct: dict = json.loads( response.content )  # type: ignore
        log.debug( f'self.post_resp_dct, ``{pprint.pformat(self.post_resp_dct)}``' )
        new_uuid: str = self.post_resp_dct['response']['referent_match_data']['uuid']
        log.debug( f'new_uuid, ``{new_uuid}``' )
        return

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


    # def delete_new_group(self):
    #     """ Deletes group used by tests."""
    #     delete_url = reverse( 'data_group_url', kwargs={'incoming_uuid': self.new_uuid} )
    #     response = self.client.delete( delete_url )
    #     self.assertEqual( 200, response.status_code )
    #     self.delete_resp_dct = json.loads( response.content )
    #     log.debug( f'delete_resp_dct, ``{pprint.pformat(self.delete_resp_dct)}``' )


    ## end Client_ReferentMatch_API_Test()




# class ReferentMatch( Base ):
#     __tablename__ = 'referent_matches'

#     uuid = Column( String(32), primary_key=True )
#     referent_A_uuid = Column( String(32), ForeignKey('5_referents.uuid') )
#     referent_B_uuid = Column( String(32), ForeignKey('5_referents.uuid') )
#     date_created = Column( DateTime() )
#     date_edited = Column( DateTime() )
#     researcher_notes = Column( UnicodeText() )
#     confidence = Column( Integer )  # optional?
