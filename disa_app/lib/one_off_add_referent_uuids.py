"""
Adds a uuid to each referent entry that doesn't have one.
- find referents without a uuid.
- for each...
    - add uuid

Usage:
- cd to project dir
- source env
- $ python3 ./disa_app/lib/one_off_add_referent_uuids.py
"""

import logging, os, sys

import django, sqlalchemy
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


## set up file logger
LOG_PATH = os.environ['DISA_DJ__LOG_PATH']
LOG_LEVEL = os.environ['DISA_DJ__LOG_LEVEL']
level_dct = { 'DEBUG': logging.DEBUG, 'INFO': logging.INFO }
logging.basicConfig(
    filename=LOG_PATH, level=level_dct[LOG_LEVEL],
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s', datefmt='%d/%b/%Y %H:%M:%S' )
log = logging.getLogger(__name__)
log.info( '\n\ngenerate-browse-data log ready' )


def manage_add_uuids() -> None:
    """ Manager for adding uuids.
        Called by if name == main... """
    log.debug( 'starting manage_add_uuids()' )
    session = make_session()
    ## get referents ------------------------------------------------
    referents_all = session.query( models_alch.Referent ).all()
    log.debug( f'referents_all count, ``{len(referents_all)}``' )
        

def make_session() -> sqlalchemy.orm.session.Session:
    """ Sets up sqlalchemy session.
        Called by manage_add_uuids() controller. """
    engine = create_engine( settings_app.DB_URL, echo=False )
    Session = sessionmaker( bind=engine )
    session = Session()
    return session




if __name__ == '__main__':
    manage_add_uuids()