import collections, datetime, json, logging, os, pathlib, pprint, sys
import django, sqlalchemy

from django.urls import reverse
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
log.info( '\n\ndenormalizer log ready' )


def main():

    session = make_session()
    filter_deleted = FilterDeleted()

    persons = session.query( models_alch.Person ).all()
    log.debug( f'persons count, ``{len(persons)}``' )

    filtered_out_deleted_persons = filter_deleted.manage_filtration( persons, session )
    log.debug( f'filtered_out_deleted_persons count, ``{len(filtered_out_deleted_persons)}``' )

    ## end def main()


# -------
# helpers
# -------


def make_session() -> sqlalchemy.orm.session.Session:
    engine = create_engine( settings_app.DB_URL, echo=False )
    Session = sessionmaker( bind=engine )
    session = Session()
    return session


class FilterDeleted():

    def __init__( self ):
        pass

    def manage_filtration( self, persons, session ):
        deleted_referent_ids = self.get_deleted_referent_ids()
        deleted_referent_objs = self.get_deleted_referent_objs( deleted_referent_ids, session )
        persons_to_ignore = self.get_persons_to_ignore( deleted_referent_objs, session )
        filtered_persons = self.apply_filter( persons, persons_to_ignore, session )
        return filtered_persons

    def apply_filter( self, persons, persons_to_ignore, session ):
        filtered_persons = []
        for person in persons:
            person_check = 'init'
            for person_to_ignore in persons_to_ignore:
                if person.id == person_to_ignore.id:
                    person_check = 'found'
                    break
            if person_check == 'init':
                filtered_persons.append( person )
            else:
                log.debug( f'filtering out person, ``{person}``' )
                person_check = 'init'
        return filtered_persons

    def get_persons_to_ignore( self, deleted_referent_objs, session ):
        persons = []
        for deleted_referent_obj in deleted_referent_objs:
            person_obj = session.query( models_alch.Person ).filter_by( id=deleted_referent_obj.person_id ).first()
            log.debug( f'for referent ``{deleted_referent_obj}``, person is, ``{person_obj}``' )
            persons.append( person_obj )
        log.debug( f'persons to ignore, ``{persons}``' )
        return persons

    def get_deleted_referent_objs( self, deleted_referent_ids, session ):
        objs = []
        for referent_id in deleted_referent_ids:
            referent_obj = session.query( models_alch.Referent ).filter_by( id=referent_id ).first()
            objs.append( referent_obj )
        log.debug( f'referent objs, ``{objs}``' )
        return objs

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

    ## end class FilterDeleted()



if __name__ == "__main__":
    main()
