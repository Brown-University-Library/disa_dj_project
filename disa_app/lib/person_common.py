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
    """ Returns display-name.
        Called by view_person_helper.query_person() """
    name: str = f'{prsn.first_name} {prsn.last_name}'.strip()
    if name == '':
        name = 'Not Listed'
    return name


def parse_person_descriptors( prsn, dscrptr ):
    """ Returns Referent descriptor value.
        Called by view_person_helper.query_person() """
    log.debug( f'person-id, `{prsn.id}`; descriptor, `{dscrptr}`' )
    vals = { desc.name for ref in prsn.references for desc in getattr(ref, dscrptr) }
    log.debug( f'vals, ```{vals}```' )
    out = ', '.join(list(vals))
    return out if out else 'Not Listed'


# def parse_person_descriptors( prsn, descriptor ):
#     vals = { desc.name for ref in personObj.references
#                 for desc in getattr(ref, descField) }
#     out = ', '.join(list(vals))
#     return out if out else 'None'


def parse_person_relations( prsn ):
    rels = [ (r.related_as, r.obj) for e in prsn.references
                for r in e.as_subject ]
    grouped = collections.defaultdict( list )
    for r in rels:
        grouped[ r[0].name_as_relationship ].append( {
            'id': r[1].person_id,
            'name': parse_person_name(r[1].person)
            } )
    calc_rels = [ { 'type': k, 'related': v } for k,v in grouped.items() ]
    log.debug( f'calc_rels, ```{pprint.pformat(calc_rels)}```' )
    return out


# def parse_person_relations(personObj):
#     rels = [ (r.related_as, r.obj) for e in personObj.references
#                 for r in e.as_subject ]
#     grouped = collections.defaultdict(list)
#     for r in rels:
#         grouped[ r[0].name_as_relationship ].append(
#             { 'id': r[1].person_id,
#             'name': parse_person_name(r[1].person) } )
#     out = [ { 'type': k, 'related': v } for k,v in grouped.items() ]
#     return out
