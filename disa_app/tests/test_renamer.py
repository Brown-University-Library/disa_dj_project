import json, logging, pprint, secrets, uuid

from django.test import SimpleTestCase as TestCase
from disa_app.lib.build_scripts.rename_js_files import Renamer

log = logging.getLogger(__name__)
TestCase.maxDiff = 1000


class Renamer_Test( TestCase ):
    """ Checks citation data-api urls. """

    def setUp(self):
        renamer = Renamer()


    def test_determine_pre_existing_hash(self):
        """ Checks extraction of existing hash. """
        filename = 'foo.js'
        self.assertEqual( 'zz', renamer.determine_pre_existing_hash( filename ) )