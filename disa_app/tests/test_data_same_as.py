""" Tests the Referent-A is the same individual as Referent-B feature/api. """

import json, logging, pprint, random

from django.test import TestCase  # TestCase requires db, so if no db is needed, try ``from django.test import SimpleTestCase as TestCase``
from django.core.urlresolvers import reverse

log = logging.getLogger(__name__)


class Client_ReferentMatch_API_Test( TestCase ):
    """ Checks `/referent_match/1234/` api urls. """

    def setUp(self):
        pass

    ## HELPERS ====================

    def create_referent_match(self):
        """ Creates a ReferentMatch entry for tests. """
        ## create referent-1
        referent_uuid_1 = self.create_new_referent()
        ## create referent-2
        referent_uuid_2 = self.create_new_referent()
        ## create referent_match entry
        post_url = reverse( 'referent_match_url' )
        log.debug( f'post-url, ``{post_url}``' )
        payload = {
            'count': 7,
            'count_estimated': True,
            'description': 'the description',
            'reference_id': 49
        }
        jsn = json.dumps( payload )
        response = self.client.post( post_url, data=jsn, content_type='application/json' )
        self.assertEqual( 200, response.status_code )
        self.post_resp_dct = json.loads( response.content )
        log.debug( f'self.post_resp_dct, ``{pprint.pformat(self.post_resp_dct)}``' )
        self.new_uuid = self.post_resp_dct['response']['group_data']['uuid']
        log.debug( f'self.new_uuid, ``{self.new_uuid}``' )

    def create_new_referent(self) -> str:
        """ Creates a referent for tests; returns UUID. """
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

    ## GET =======================

    ## CREATE ====================

    ## UPDATE ====================

    ## DELETE ====================

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
