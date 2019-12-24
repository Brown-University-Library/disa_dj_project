# -*- coding: utf-8 -*-

import datetime, json, logging, os, pprint

# import sqlalchemy
# from disa_app import settings_app
# from disa_app import models_sqlalchemy as models_alch
# from django.conf import settings
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker


log = logging.getLogger(__name__)


# def make_session() -> sqlalchemy.orm.session.Session:
#     engine = create_engine( settings_app.DB_URL, echo=True )
#     Session = sessionmaker( bind=engine )
#     session = Session()
#     return session


def parse_person_name( prsn ) -> str:
    log.debug( f'type(prsn), ```{type(prsn)}```' )
    log.debug( f'prsn.__dict__, ```{prsn.__dict__}```' )
    log.debug( f'prsn.references, ```{prsn.references}```' )
    name: str = f'{prsn.first_name} {prsn.last_name}'.strip()
    if name == '':
        name = 'Not Listed'
    return name


def parse_person_descriptors( prsn, descriptor ):
    vals = { desc.name for ref in prsn.references for desc in getattr(ref, descField) }
    log.debug( f'vals, ```{vals}```' )
    out = ', '.join(list(vals))
    return out if out else 'None'


# def parse_person_descriptors( prsn, descriptor ):
#     vals = { desc.name for ref in personObj.references
#                 for desc in getattr(ref, descField) }
#     out = ', '.join(list(vals))
#     return out if out else 'None'
