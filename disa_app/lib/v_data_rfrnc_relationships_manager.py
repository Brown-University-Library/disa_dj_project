# -*- coding: utf-8 -*-

import datetime, json, logging, os, pprint

import sqlalchemy
from disa_app import settings_app
from disa_app import models_sqlalchemy as models_alch
from disa_app.lib import person_common
from django.conf import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


log = logging.getLogger(__name__)


def make_session() -> sqlalchemy.orm.session.Session:
    engine = create_engine( settings_app.DB_URL, echo=True )
    Session = sessionmaker( bind=engine )
    session = Session()
    return session


def prepare_data( rfrnc_id: str ):
    """ Handles ajax api call for relationships_by_reference data.
        Called by views.relationships_by_reference()
        """
    log.debug( f'rfrnc_id, ```{rfrnc_id}```' )
    session = make_session()
    data = {}

    rfrnc = session.query( models_alch.Reference ).get( rfrnc_id )

    referents = [ { 'id': e.id, 'name': e.display_name() }
        for e in rfrnc.referents ]



    # relationships = [ { 'id': r.id, 'name': r.name_as_relationship }
    #     for r in models.Role.query.all()
    #     if r.name_as_relationship is not None ]

    relationships = [ { 'id': r.id, 'name': r.name_as_relationship }
        for r in session.query( models_alch.Role ).all() if r.name_as_relationship is not None
        ]

    # all_roles = session.query( models_alch.Role ).all()



    rnt_map = { f['id']: f['name'] for f in referents }
    rel_map = { r['id']: r['name'] for r in relationships }
    store = [
        {
        'id': r.id,
        'data':
            {
            'sbj': { 'name': rnt_map[r.subject_id], 'id': r.subject_id },
            'rel': { 'name': rel_map[r.role_id], 'id': r.role_id },
            'obj': { 'name': rnt_map[r.object_id], 'id': r.object_id }
            }
        }
        for f in rfrnc.referents
            for r in f.as_subject
    ]
    data = { 'store': store, 'people': referents,
        'relationships': relationships }



    log.debug( f'data, ```{pprint.pformat(data)}```' )
    return data


## from DISA
# @app.route('/data/sections/<refId>/relationships/')
# @login_required
# def relationships_by_reference(refId):
#     ref = models.Reference.query.get(refId)
#     referents = [ { 'id': e.id, 'name': e.display_name() }
#         for e in ref.referents ]
#     relationships = [ { 'id': r.id, 'name': r.name_as_relationship }
#         for r in models.Role.query.all()
#         if r.name_as_relationship is not None ]
#     rnt_map = { f['id']: f['name'] for f in referents }
#     rel_map = { r['id']: r['name'] for r in relationships }
#     store = [
#         {
#         'id': r.id,
#         'data':
#             {
#             'sbj': { 'name': rnt_map[r.subject_id], 'id': r.subject_id },
#             'rel': { 'name': rel_map[r.role_id], 'id': r.role_id },
#             'obj': { 'name': rnt_map[r.object_id], 'id': r.object_id }
#             }
#         }
#         for f in ref.referents
#             for r in f.as_subject
#     ]
#     data = { 'store': store, 'people': referents,
#         'relationships': relationships }
#     return jsonify(data)
