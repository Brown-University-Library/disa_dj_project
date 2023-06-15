"""
Usage:
- $ cd /to/project_root (where manage.py is)
- $ python ./disa_app.lib.build_scripts.rename_js_files
"""

import os
import logging
import pprint
import re
import subprocess
import hashlib


logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s', 
    datefmt='%d/%b/%Y %H:%M:%S' )
log = logging.getLogger(__name__)


EXCLUDES = [
    'hilitor.js',
    'lunr.min.js',
    'moment.js',
    'tabulator.js',
    'tagify.min.js',
    'tinymce-vue.js',
]


class Renamer():

    def __init__(self) -> None:
        self.tracker_dict = {}
        self.js_dir_path = ''  # set in get_relevant_file_paths()
        self.temp_renamed_filename = ''

    def manage_renames( self, project_directory ):
        """ Controller function.
            Called by dunder-main. """
        log.debug( 'starting manage_renames()' )
        ## prep list relevant files ---------------------------------
        self.get_relevant_file_paths( project_directory )  # initializes self.tracker_dict
        ## run file-renames -----------------------------------------
        for filename, file_info in self.tracker_dict.items():
            self.rename_file( filename, file_info )
        return

    ## main helper functions ----------------------------------------

    def get_relevant_file_paths( self, project_dir_path: str ) -> None:
        """ Compiles list of relevant file-paths.
            Initializes tracker-dict.
            Called by main() """
        log.debug( f'project_dir_path, ``{project_dir_path}``' ); assert type(project_dir_path) == str
        ## identify js-directory ------------------------------------
        js_dir_path = os.path.join(project_dir_path, "disa_app/static/js/"); assert type(js_dir_path) == str
        log.debug( f'js_dir_path, ``{js_dir_path}``' )
        if not os.path.exists(js_dir_path):
            raise Exception( f"Directory ``{js_dir_path}`` does not exist." )
        self.js_dir_path = js_dir_path
        ## identify relevant files ----------------------------------
        dir_contents: list = os.listdir(js_dir_path)
        log.debug( f'dir_contents, ``{pprint.pformat(dir_contents)}``' )
        for entry in dir_contents:
            log.debug( f'processing entry, ``{entry}``' )
            if entry.endswith('.js'):
                if entry in EXCLUDES:
                    log.debug( f'skipping excluded file, ``{entry}``' )
                    continue
                ## add to tracker-dict ------------------------------
                self.tracker_dict[entry] = {}
                self.tracker_dict[entry]['file_path'] = os.path.join(js_dir_path, entry)
        log.debug( f'tracker_dict after initialization, ``{pprint.pformat(self.tracker_dict)}``' )
        return

    def rename_file( self, filename: str, file_info: dict ):
        """ Coordinates filename rename step.
            Called by manage_renames(). """
        log.debug( 'starting rename_file()' ); assert type(filename) == str; assert type(file_info) == dict
        file_path: str = file_info['file_path']; assert type(file_path) == str
        log.debug( f'processing file_path, ``{file_path}``' )
        ## determine pre-existing hash ------------------------------
        pre_existing_hash: str = self.determine_pre_existing_hash( filename ); assert type(pre_existing_hash) == str
        ## determine actual hash ------------------------------------
        actual_hash: str = self.determine_md5_hash( file_path ); assert type(actual_hash) == str

        ## rename file if needed ------------------------------------
        log.debug( f'tracker_dict after rename, ``{pprint.pformat(self.tracker_dict)}``' )    

        ## rename references ----------------------------------------
        ## TODO

        return
    
        ## sub-helper functions -------------------------------------

    def determine_pre_existing_hash( self, filename: str ) -> str:
        """ Returns pre-existing hash from filename.
            Called by rename_file() """
        assert type(filename) == str
        pre_existing_hash: str = ''
        match_obj = re.search(r'__(\w+)\.js', filename)
        assert ( match_obj is None ) or ( type(match_obj) == re.Match )
        log.debug( f'match_obj, ``{match_obj}``' )
        if match_obj:
            pre_existing_hash = match_obj.group(1); assert type(pre_existing_hash) == str
            log.debug( f'pre_existing_hash, ``{pre_existing_hash}``' )
        else:
            log.debug( f'no pre-existing hash found in filename, ``{filename}``' )
        return pre_existing_hash

    def determine_md5_hash( self, file_path: str ) -> str:
        """ Returns md5 hash of file.
            Called by rename_file() """
        assert type(file_path) == str
        hash_md5 = hashlib.md5()
        with open( file_path, 'rb' ) as f:
            for chunk in iter( lambda: f.read(4096), b'' ):
                hash_md5.update( chunk )
        return_hash: str = hash_md5.hexdigest(); assert type(return_hash) == str
        log.debug( f'return_hash, ``{return_hash}``' )
        return return_hash

    # def rename_if_needed(self, filename, filepath, previous_hash, actual_hash):
    #     base_filename, extension = os.path.splitext(filename)
    #     if previous_hash in base_filename:
    #         new_filename = base_filename.replace(previous_hash, actual_hash) + extension
    #     else:
    #         new_filename = f'{base_filename}__{actual_hash}{extension}'
    #     new_filepath = os.path.join(os.path.dirname(filepath), new_filename)
    #     os.rename(filepath, new_filepath)

    def rename_if_needed( self, filename: str, file_path: str, pre_existing_hash: str, actual_hash: str ) -> str:
        """ Renames file if needed. 
            Called by rename_file() """
        assert type(filename) == str; assert type(file_path) == str; assert type(pre_existing_hash) == str; assert type(actual_hash) == str
        log.debug( f'filename, ``{filename}``; file_path, ``{file_path}``; pre_existing_hash, ``{pre_existing_hash}``; actual_hash, ``{actual_hash}``')
        new_filename = ''
        base_filename, extension = os.path.splitext( filename )
        log.debug( f'base_filename, ``{base_filename}``; extension, ``{extension}``' )
        if pre_existing_hash == '':  # eg "foo.js"
            log.debug( 'no pre-existing hash' )
            new_filename = f'{base_filename}__{actual_hash}{extension}'
        else:
            if pre_existing_hash in base_filename:
                if pre_existing_hash != actual_hash:
                    log.debug( 'hashes do not match; renaming' )
                    # new_filename = f'{base_filename}__{actual_hash}{extension}'
                    new_filename = base_filename.replace(pre_existing_hash, actual_hash) + extension
                else:
                    log.debug( 'hashes match; not renaming' )
                    new_filename = ''
                # new_filename = base_filename.replace(pre_existing_hash, actual_hash) + extension
        log.debug( f'new_filename, ``{new_filename}``' )
        ## perform rename -------------------------------------------
        if new_filename:
            new_filepath = os.path.join( os.path.dirname(file_path), new_filename )
            os.rename(file_path, new_filepath)
        else:
            log.debug( 'no filename; not renaming' )
        return new_filename

    # def rename_if_needed( self, filename: str, file_path: str, pre_existing_hash: str, actual_hash: str ) -> None:
    #     """ Renames file if needed. 
    #         Called by rename_file() """
    #     assert type(filename) == str; assert type(file_path) == str; assert type(pre_existing_hash) == str; assert type(actual_hash) == str
    #     log.debug( f'filename, ``{filename}``; file_path, ``{file_path}``; pre_existing_hash, ``{pre_existing_hash}``; actual_hash, ``{actual_hash}``')
    #     base_filename, extension = os.path.splitext(filename)
    #     if pre_existing_hash != actual_hash:
    #         new_filename = f'{base_filename}__{actual_hash}{extension}'
    #         new_filepath = os.path.join(os.path.dirname(file_path), new_filename)
    #         os.rename(file_path, new_filepath)
    #         self.temp_renamed_filename = new_filename
    #     else:
    #         self.temp_renamed_filename = filename
    #     return

    
    ## end class Renamer()


    # def rename_files( self ):
    #     """ Coordinate filename rename step.
    #         Called by manage_renames(). """
    #     log.debug( 'starting rename_files()' )
    #     for filename, file_info in self.tracker_dict.items():
    #         assert type(filename) == str
    #         assert type(file_info) == dict
    #         file_path = file_info['file_path']; assert type(file_path) == str
    #         log.debug( f'processing file_path, ``{file_path}``' )
    #         ## look for pre-existing hash -------------------------------
    #         match_obj = re.search(r'__(\w+)\.js', filename)
    #         assert match_obj is None or type(match_obj) == re.Match
    #         log.debug( f'match_obj, ``{match_obj}``' )
    #         if match_obj:
    #             # assert type(match_obj) == re.Match
    #             pre_existing_hash = match_obj.group(1); assert type(pre_existing_hash) == str
    #             log.debug( f'pre_existing_hash, ``{pre_existing_hash}``' )
    #             self.tracker_dict[filename]['pre_existing_hash'] = pre_existing_hash
                
    #             # actual_hash = md5(file_path)
    #         else:
    #             log.debug( f'no pre-existing hash found in filename, ``{filename}``' )
    #             self.tracker_dict[filename]['pre_existing_hash'] = None


    #         # 2/0
        
    #         # if actual_hash != pre_existing_hash:
    #         #     new_filename = re.sub(r'__(\w+)\.js', f'__{actual_hash}.js', filename)
    #         #     new_file_path = os.path.join(js_directory, new_filename)
    #         #     log.debug( f'new_file_path, ``{new_file_path}``' )
    #         #     os.rename(file_path, new_file_path)
    #         #     update_references(project_directory, filename, new_filename)
    #         #     log.debug(f"Updated {filename} to {new_filename}")
    #         # else:
    #         #     log.debug(f"Hash matched for {filename}")

    #     log.debug( f'tracker_dict after rename, ``{pprint.pformat(self.tracker_dict)}``' )    
    #     return



# def rename_file(file_path, new_filename):
#         if actual_hash != pre_existing_hash:
#             new_filename = re.sub(r'__(\w+)\.js', f'__{actual_hash}.js', filename)
#             new_file_path = os.path.join(js_directory, new_filename)
#             log.debug( f'new_file_path, ``{new_file_path}``' )
#             os.rename(file_path, new_file_path)
#             update_references(project_directory, filename, new_filename)
#             log.debug(f"Updated {filename} to {new_filename}")
#         else:
#             log.debug(f"Hash matched for {filename}")



# def update_references(directory, old_filename, new_filename):
#     for foldername, subfolders, filenames in os.walk(directory):
#         for filename in filenames:
#             file_path = os.path.join(foldername, filename)
#             with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
#                 filedata = file.read()
            
#             # Replace the target string
#             new_data = filedata.replace(old_filename, new_filename)
            
#             # Write the file out again
#             with open(file_path, 'w', encoding='utf-8', errors='ignore') as file:
#                 file.write(new_data)


    # for filename in os.listdir(js_directory):
    #     if filename.endswith('.js'):
    #         file_path = os.path.join(js_directory, filename)
    #         log.debug( f'file_path, ``{file_path}``' )
    #         pre_existing_hash = re.search(r'__(\w+)\.js', filename)
    #         log.debug( f'pre_existing_hash, ``{pre_existing_hash}``' )
    #         if pre_existing_hash:
    #             pre_existing_hash = pre_existing_hash.group(1)
    #             actual_hash = md5(file_path)

    #         else:
    #             log.debug(f"File {filename} does not have a pre-existing hash in its name")


if __name__ == "__main__":
    log.debug( '\n\nstarting dunder-main' )
    renamer = Renamer()
    PROJECT_DIR_PATH = os.curdir; assert type(PROJECT_DIR_PATH) == str  
    project_dir_fullpath = os.path.abspath(PROJECT_DIR_PATH); assert type(project_dir_fullpath) == str
    log.debug( f'project_dir_fullpath, ``{project_dir_fullpath}``' )
    renamer.manage_renames( project_dir_fullpath )
