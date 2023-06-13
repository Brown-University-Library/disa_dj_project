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

    def manage_renames( self, project_directory ):
        """ Controller function.
            Called by dunder-main. """
        log.debug( 'starting manage_renames()' )
        ## prep list relevant files ---------------------------------
        self.get_relevant_file_paths( project_directory )  # initializes self.tracker_dict

        ## run file-renames -----------------------------------------
        self.rename_files()

        ## run reference-updates ------------------------------------
        #TODO

        return

    def rename_files( self ):
        """ Coordinate filename rename step.
            Called by manage_renames(). """
        log.debug( 'starting rename_files()' )
        for filename, file_info in self.tracker_dict.items():
            assert type(filename) == str
            assert type(file_info) == dict
            file_path = file_info['file_path']; assert type(file_path) == str
            log.debug( f'processing file_path, ``{file_path}``' )
            ## look for pre-existing hash -------------------------------
            match_obj = re.search(r'__(\w+)\.js', filename)
            assert match_obj is None or type(match_obj) == re.Match
            log.debug( f'match_obj, ``{match_obj}``' )
            if match_obj:
                # assert type(match_obj) == re.Match
                pre_existing_hash = match_obj.group(1); assert type(pre_existing_hash) == str
                log.debug( f'pre_existing_hash, ``{pre_existing_hash}``' )
                self.tracker_dict[filename]['pre_existing_hash'] = pre_existing_hash
                
                # actual_hash = md5(file_path)
            else:
                log.debug( f'no pre-existing hash found in filename, ``{filename}``' )
                self.tracker_dict[filename]['pre_existing_hash'] = None


            # 2/0
        
            # if actual_hash != pre_existing_hash:
            #     new_filename = re.sub(r'__(\w+)\.js', f'__{actual_hash}.js', filename)
            #     new_file_path = os.path.join(js_directory, new_filename)
            #     log.debug( f'new_file_path, ``{new_file_path}``' )
            #     os.rename(file_path, new_file_path)
            #     update_references(project_directory, filename, new_filename)
            #     log.debug(f"Updated {filename} to {new_filename}")
            # else:
            #     log.debug(f"Hash matched for {filename}")

        log.debug( f'tracker_dict after rename, ``{pprint.pformat(self.tracker_dict)}``' )    
        return

    def get_relevant_file_paths( self, project_dir_path: str ) -> None:
        """ Compiles list of relevant file-paths.
            Initializes tracker-dict.
            Called by main() """
        log.debug( f'project_dir_path, ``{project_dir_path}``' )
        ## identify js-directory ------------------------------------
        js_dir_path = os.path.join(project_dir_path, "disa_app/static/js/")
        log.debug( f'js_dir_path, ``{js_dir_path}``' )
        if not os.path.exists(js_dir_path):
            raise Exception( f"Directory ``{js_dir_path}`` does not exist." )
            return
        assert type(js_dir_path) == str
        log.debug( f'js_directory_path, ``{js_dir_path}``' )
        dir_contents: list = os.listdir(js_dir_path)
        log.debug( f'dir_contents, ``{pprint.pformat(dir_contents)}``' )
        ## identify relevant files ----------------------------------
        for entry in dir_contents:
            log.debug( f'processing entry, ``{entry}``' )
            if entry.endswith('.js'):
                if entry in EXCLUDES:
                    log.debug( f'skipping excluded file, ``{entry}``' )
                    continue
                ## add to tracker-dict ------------------------------
                self.tracker_dict[entry] = {}
                file_path = os.path.join(js_dir_path, entry)
                self.tracker_dict[entry]['file_path'] = file_path
        log.debug( f'tracker_dict after initialization, ``{pprint.pformat(self.tracker_dict)}``' )
        return


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

# def md5(file_path):
#     hash_md5 = hashlib.md5()
#     with open(file_path, "rb") as f:
#         for chunk in iter(lambda: f.read(4096), b""):
#             hash_md5.update(chunk)
#     return hash_md5.hexdigest()


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
