import json, logging, os, shutil

from django.test import SimpleTestCase as TestCase
from disa_app.lib.build_scripts.rename_js_files import Renamer

log = logging.getLogger(__name__)
TestCase.maxDiff = 1000


class Renamer_Test( TestCase ):
    """ Checks Renamer() functions. """

    def setUp(self):
        self.renamer = Renamer()
        self.helper__clear_test_directory()  # only needed for test_rename()

    def test_determine_pre_existing_hash(self):
        """ Checks extraction of existing hash. """
        filename = 'foo.js'
        self.assertEqual( '', self.renamer.determine_pre_existing_hash( filename ) )
        filename = 'foo__abc.js'
        self.assertEqual( 'abc', self.renamer.determine_pre_existing_hash( filename ) )
        filename = 'foo-bar__def.js'
        self.assertEqual( 'def', self.renamer.determine_pre_existing_hash( filename ) )

    def test_determine_actual_hash(self):
        """ Checks actual hash. """
        filepath = './disa_app/static/js/browse_tabulator.js'
        self.assertEqual( 'e8c2913fb1f278a73804145e3cfc3739', self.renamer.determine_md5_hash( filepath ) )

    def test_rename_if_needed(self):
        """ Checks renaming."""
        filename = 'foo__abc.js'
        filepath = f'./disa_app/tests/test_renamer_files/{filename}'
        previous_hash = 'abc'
        actual_hash = 'def'
        self.renamer.rename_if_needed( filename, filepath, previous_hash, actual_hash )
        self.assertEqual( 'foo__.def', self.renamer.temp_renamed_filename )

    ## helper -------------------------------------------------------

    def helper__clear_test_directory(self):
        """ Clears test directory. """
        ## specify the directory path -------------------------------
        directory_path = './disa_app/tests/test_renamer_files'
        ## confirm path ---------------------------------------------
        if os.path.exists( directory_path):
            if not os.path.isdir( directory_path):
                raise Exception( f'the path ``{directory_path}`` exists but is not a directory.' )
        else:
            raise Exception( f'the path ``{directory_path}`` does not exist.' ) 
        ## remove directory contents --------------------------------
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        ## create an empty file -------------------------------------
        with open(os.path.join(directory_path, 'foo.js'), 'w') as file:
            pass
        ## create second 'uses_foo.js' ------------------------------
        with open(os.path.join(directory_path, 'uses_foo.js'), 'w') as file:
            file.write('import "./foo.js";\n')
        return
    
    ## end class Renamer_Test()
