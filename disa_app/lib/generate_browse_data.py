# -*- coding: utf-8 -*-

"""
Creates the json file used by the browse-table javascript library.

Usage...
- called by cron script in practice.
- can be called manually by cd-ing to the project directory (with virtual-environment activated) and running:
  $ python3 ./disa_app/lib/generate_browse_data.py
"""

import collections, datetime, json, logging, os, pathlib, pprint, sys
import django, sqlalchemy

from django.core.urlresolvers import reverse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

## configure django paths
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
cwd = os.getcwd()  # assumes the cwd is the project directory
if cwd not in sys.path:
    sys.path.append( cwd )
django.setup()

## ok, now django-related imports will work
from disa_app import models_sqlalchemy as models_alch
from disa_app import settings_app
from disa_app.models import MarkedForDeletion


## set up file logger
LOG_PATH = os.environ['DISA_DJ__LOG_PATH']
LOG_LEVEL = os.environ['DISA_DJ__LOG_LEVEL']
level_dct = { 'DEBUG': logging.DEBUG, 'INFO': logging.INFO }
logging.basicConfig(
    filename=LOG_PATH, level=level_dct[LOG_LEVEL],
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s', datefmt='%d/%b/%Y %H:%M:%S' )
log = logging.getLogger(__name__)
log.info( '\n\ngenerate-browse-data log ready' )


def manage_generation():
    """ Produces json used by 'browse'.
        Called by ```if __name__ == "__main__":``` """
    log.debug( 'starting json_for_browse()' )
    start_time = datetime.datetime.now()
    session = make_session()

    referents_all = session.query( models_alch.Referent ).all()
    log.debug( f'referents_all count, ``{len(referents_all)}``' )

    filter_deleted = FilterDeleted()
    referents = filter_deleted.manage_filtration( referents_all, session )
    log.debug( f'referents after deletion-removal, ``{len(referents)}``' )

    ( output_dct, initialized_referent_dct ) = initialize_output()
    for referent in referents:
        populate_output( referent, output_dct, initialized_referent_dct )

    log.debug( f'output_dct, ``{pprint.pformat(output_dct)}``' )
    return output_dct

    ## end manage_generation()


def make_session() -> sqlalchemy.orm.session.Session:
    engine = create_engine( settings_app.DB_URL, echo=False )
    Session = sessionmaker( bind=engine )
    session = Session()
    return session


def initialize_output() -> tuple:
    """ Sets up structs for ouput.
        Listed here for visual clarity.
        Called by manage_generation() """
    initialized_output_dct = {
        'meta': {
            'date_produced': str( datetime.datetime.now() ),
            'referent_count': None,
            'excluded_referent_counts': None,
        },
        'referent_list': [
        ]
    }
    initialized_referent_dct = {
        'id': '',
        'uuid': '',
        'name_first': '',
        'name_last': '',

        'tribe': '',
        'sex': '',
        'origin': '',
        'vocation': '',
        'age': '',
        'race': '',
        'title': '',

        'citation_data': {},
        'reference_data': {},
    }
    return ( initialized_output_dct, initialized_referent_dct )

def populate_output( referent, output_dct, initialized_referent_dct ):
    if len( output_dct['referent_list'] ) > 5:
        1/0
    referent_dct = initialized_referent_dct.copy()
    referent_dct['id'] = referent.id
    referent_dct['uuid'] = '(unavailable)'
    ( first_name, last_name ) = get_name( referent )
    referent_dct['name_first'] = first_name
    referent_dct['name_last'] = last_name
    output_dct['referent_list'].append( referent_dct )
    return

def get_name( referent ):
    log.debug( f'referent.names, ``{referent.names}``' )

    for name in referent.names:
        log.debug( f'referent-name.name_type, ``{name.name_type}``')

    name = referent.names[0]
    name_tuple = ( name.first, name.last )
    log.debug( f'name_tuple, ``{name_tuple}``' )
    return name_tuple




class FilterDeleted():

    def __init__( self ):
        self.deleted_referent_ids = None  # added this for output dct

    def manage_filtration( self, referents_all, session ):
        deleted_referent_ids = self.get_deleted_referent_ids()
        self.deleted_referent_ids = deleted_referent_ids
        referents_to_ignore = self.get_deleted_referent_objs( deleted_referent_ids, session )
        # persons_to_ignore = self.get_persons_to_ignore( deleted_referent_objs, session )
        filtered_referents = self.apply_filter( referents_all, referents_to_ignore, session )
        return filtered_referents

    def get_deleted_referent_ids( self ):
        referent_ids = []
        marked_entries = MarkedForDeletion.objects.all()
        for entry in marked_entries:
            doc = json.loads( entry.doc_json_data )
            references = doc.get( 'references', None )
            if references:
                for reference in references:
                    referents = reference.get( 'referents', None )
                    if referents:
                        for referent in referents:
                            referent_ids.append( referent['id'] )
        sorted_referent_ids = sorted( referent_ids )
        log.debug( f'referent_ids, ``{sorted_referent_ids}``' )
        return sorted_referent_ids

    def get_deleted_referent_objs( self, deleted_referent_ids, session ):
        objs = []
        for referent_id in deleted_referent_ids:
            referent_obj = session.query( models_alch.Referent ).filter_by( id=referent_id ).first()
            objs.append( referent_obj )
        log.debug( f'referent objs, ``{objs}``' )
        return objs

    def apply_filter( self, referents_all, referents_to_ignore, session ):
        filtered_referents = []
        for referent in referents_all:
            referent_check = 'init'
            for referent_to_ignore in referents_to_ignore:
                if referent.id == referent_to_ignore.id:
                    referent_check = 'ignore'
                    break
            if referent_check == 'init':
                filtered_referents.append( referent )
            else:
                log.debug( f'filtering out referent, ``{referent}``' )
                referent_check = 'init'
        return filtered_referents

    ## end class FilterDeleted()


if __name__ == '__main__':
    output = manage_generation()
    unformatted_output_path = os.environ[ 'DISA_DJ__BROWSE_JSON_PATH' ]
    log.debug( f'unformatted_output_path, ``{unformatted_output_path}``' )  # logging not currently working
    formatted_output_path = f'%s/browse_data_formatted.json' % pathlib.Path( settings_app.DISA_DJ__BROWSE_JSON_PATH ).parent
    log.debug( f'formatted_output_path, ``{formatted_output_path}``' )
    log.debug( f'type(output), ``{type(output)}``' )
    jsn = json.dumps( output )
    pretty_jsn = json.dumps( output, sort_keys=True, indent=2 )
    with open( unformatted_output_path, 'w' ) as f:
        f.write( jsn )
    with open( formatted_output_path, 'w' ) as f2:
        f2.write( pretty_jsn )
