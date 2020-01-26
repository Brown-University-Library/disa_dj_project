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


def prepare_relationships_by_reference_data( rfrnc_id: str ):
    """ Handles ajax api call for relationships_by_reference data.
        Called by views.relationships_by_reference()
        """
    log.debug( f'rfrnc_id, ```{rfrnc_id}```' )
    session = make_session()
    data = {}
    rfrnc = session.query( models_alch.Reference ).get( rfrnc_id )
    referents = [ { 'id': e.id, 'name': e.display_name() }
        for e in rfrnc.referents ]
    relationships = [ { 'id': r.id, 'name': r.name_as_relationship }
        for r in session.query( models_alch.Role ).all() if r.name_as_relationship is not None
        ]
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



def manage_relationships_post( payload: bytes, request_user_id: int ) -> str:
    """ Handles ajax api call; creates relationship entry.
        Called by views.data_relationships() """
    log.debug( 'starting manage_relationships_post()' )
    self.session = make_session()
    # self.common = Common()
    data: dict = json.loads( payload )

    rfrnc_id = ''
    try:
        section: int = data['section']  # seems to be the 'reference-id'
        rfrnc = session.query( models_alch.Reference ).get( section )

        existing = session.query( models_alch.ReferentRelationship ).filter_by(
            subject_id=data['sbj'], role_id=data['rel'],
            object_id=data['obj']).first()
        log.debug( 'type(existing), ```{type(existing)}```' )

        #     existing = models.ReferentRelationship.query.filter_by(
        #         subject_id=data['sbj'], role_id=data['rel'],
        #         object_id=data['obj']).first()

    except:
        log.exception( 'problem creating relationship...' )

    return rfrnc_id




## from DISA -- POST
# @app.route('/data/relationships/', methods=['POST'])
# @login_required
# def create_relationship():
#     log.debug( 'starting create_relationship()' )
#     data = request.get_json()
#     ref = models.Reference.query.get(data['section'])
#     existing = models.ReferentRelationship.query.filter_by(
#         subject_id=data['sbj'], role_id=data['rel'],
#         object_id=data['obj']).first()
#     if not existing:
#         relt = models.ReferentRelationship(
#             subject_id=data['sbj'], role_id=data['rel'],
#             object_id=data['obj'])
#         db.session.add(relt)
#         implied = relt.entailed_relationships()
#         for i in implied:
#             existing = models.ReferentRelationship.query.filter_by(
#                 subject_id=i.subject_id, role_id=i.role_id,
#                 object_id=i.object_id).first()
#             if not existing:
#                 db.session.add(i)
#         db.session.commit()
#         stamp_edit(current_user, ref)
#     return redirect(
#         url_for('relationships_by_reference', refId = ref.id),
#         code=303 )



## from DISA -- GET
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
