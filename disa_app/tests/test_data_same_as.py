""" Tests the Referent-A is the same individual as Referent-B feature/api. """

import json, logging, pprint, secrets

from django.test import TestCase  # TestCase requires db, so if no db is needed, try ``from django.test import SimpleTestCase as TestCase``
from django.core.urlresolvers import reverse

log = logging.getLogger(__name__)


class Client_ReferentMatch_API_Test( TestCase ):
    """ Checks `/referent_match/1234/` api urls. """

    def setUp(self):
        pass

    # ## HELPERS ====================

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
