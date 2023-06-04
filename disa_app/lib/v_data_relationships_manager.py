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
    rfrnc = session.query( models_alch.Reference ).get( rfrnc_id )
    referents = [ { 'id': e.id, 'name': e.display_name() }
        for e in rfrnc.referents ]
    relationships = [ { 'id': r.id, 'name': r.name_as_relationship }
        for r in session.query( models_alch.Role ).all() if r.name_as_relationship is not None ]
    rnt_map = { f['id']: f['name'] for f in referents }
    rel_map = { r['id']: r['name'] for r in relationships }
    store = [ {
        'id': r.id,
        'data': {
            'sbj': { 'name': rnt_map[r.subject_id], 'id': r.subject_id },
            'rel': { 'name': rel_map[r.role_id], 'id': r.role_id },
            'obj': { 'name': rnt_map[r.object_id], 'id': r.object_id }
            } }
        for f in rfrnc.referents
            for r in f.as_subject ]
    data = { 'store': store, 'people': referents, 'relationships': relationships }
    log.debug( f'data, ```{pprint.pformat(data)}```' )
    return data

    ## end prepare_relationships_by_reference_data()


def manage_relationships_post( payload: bytes, request_user_id: int ) -> dict:
    """ Handles ajax api call; creates relationship entry.
        Called by views.data_relationships() """
    log.debug( 'starting manage_relationships_post()' )
    return_dct = {
        'rfrnc_id': None,
        'relationship_id': None,
        'relationship_is_new': None,
    }
    try:
        session = make_session()
        data: dict = json.loads( payload )
        log.debug( f'data, ``{pprint.pformat(data)}``' )
        section: int = data['section']  # seems to be the 'reference-id'
        rfrnc = session.query( models_alch.Reference ).get( section )
        rfrnc_id: int = rfrnc.id
        assert type(rfrnc_id) == int
        return_dct['rfrnc_id'] = rfrnc_id
        existing = session.query( models_alch.ReferentRelationship ).filter_by(
            subject_id=data['sbj'], role_id=data['rel'],
            object_id=data['obj']
            ).first()
        if not existing:
            log.debug( 'relationship does not exist; will create it' )
            add_posted_relationships( data, request_user_id, rfrnc, session )
            return_dct['relationship_id'] = 9999
            return_dct['relationship_is_new'] = True
        else:
            log.debug( 'relationship already exists' )
            log.debug( f'existing.__dict__, ``{pprint.pformat(existing.__dict__)}``' )
            log.debug( f'existing.id, ``{existing.id}``' )
            log.debug( f'type(existing.id), ``{type(existing.id)}``' )
            assert type( existing.id ) == int
            return_dct['relationship_id'] = existing.id
            return_dct['relationship_is_new'] = False
        assert type( return_dct['rfrnc_id'] ) == int
        assert type( return_dct['relationship_id'] ) == int
        assert type( return_dct['relationship_is_new'] ) == bool
        log.debug( f'return_dct, ``{pprint.pformat(return_dct)}``' )
    except Exception as e:
        log.exception( 'problem with post...' )
        raise Exception( f'exception, ```{e}```' )
    return return_dct


# def manage_relationships_post( payload: bytes, request_user_id: int ) -> str:
#     """ Handles ajax api call; creates relationship entry.
#         Called by views.data_relationships() """
#     log.debug( 'starting manage_relationships_post()' )
#     try:
#         session = make_session()
#         data: dict = json.loads( payload )
#         log.debug( f'data, ``{pprint.pformat(data)}``' )
#         section: int = data['section']  # seems to be the 'reference-id'
#         rfrnc = session.query( models_alch.Reference ).get( section )
#         rfrnc_id = rfrnc.id
#         existing = session.query( models_alch.ReferentRelationship ).filter_by(
#             subject_id=data['sbj'], role_id=data['rel'],
#             object_id=data['obj']).first()
#         if not existing:
#             log.debug( 'relationship does not exist; will create it' )
#             add_posted_relationships( data, request_user_id, rfrnc, session )
#         else:
#             log.debug( 'relationship already exists' )
#             log.debug( f'existing.__dict__, ``{pprint.pformat(existing.__dict__)}``' )
#     except Exception as e:
#         log.exception( 'problem with post...' )
#         raise Exception( f'exception, ```{e}```' )
#     log.debug( f'returning rfrnc_id for redirect, `{rfrnc_id}`' )
#     return rfrnc_id


# def manage_relationships_post( payload: bytes, request_user_id: int ) -> str:
#     """ Handles ajax api call; creates relationship entry.
#         Called by views.data_relationships() """
#     log.debug( 'starting manage_relationships_post()' )
#     try:
#         session = make_session()
#         data: dict = json.loads( payload )
#         log.debug( f'data, ``{pprint.pformat(data)}``' )
#         section: int = data['section']  # seems to be the 'reference-id'
#         rfrnc = session.query( models_alch.Reference ).get( section )
#         rfrnc_id = rfrnc.id
#         existing = session.query( models_alch.ReferentRelationship ).filter_by(
#             subject_id=data['sbj'], role_id=data['rel'],
#             object_id=data['obj']).first()
#         if not existing:
#             log.debug( 'relationship does not exist; will create it' )
#             add_posted_relationships( data, request_user_id, rfrnc, session )
#         else:
#             log.debug( 'relationship already exists' )
#             log.debug( f'existing.__dict__, ``{pprint.pformat(existing.__dict__)}``' )
#     except Exception as e:
#         log.exception( 'problem with post...' )
#         raise Exception( f'exception, ```{e}```' )
#     log.debug( f'returning rfrnc_id for redirect, `{rfrnc_id}`' )
#     return rfrnc_id


# def manage_relationships_post( payload: bytes, request_user_id: int ) -> str:
#     """ Handles ajax api call; creates relationship entry.
#         Called by views.data_relationships() """
#     log.debug( 'starting manage_relationships_post()' )
#     try:
#         session = make_session()
#         data: dict = json.loads( payload )
#         log.debug( f'data, ``{pprint.pformat(data)}``' )
#         section: int = data['section']  # seems to be the 'reference-id'
#         rfrnc = session.query( models_alch.Reference ).get( section )
#         rfrnc_id = rfrnc.id
#         existing = session.query( models_alch.ReferentRelationship ).filter_by(
#             subject_id=data['sbj'], role_id=data['rel'],
#             object_id=data['obj']).first()
#         if not existing:
#             add_posted_relationships( data, request_user_id, rfrnc, session )
#     except:
#         log.exception( 'problem with post...' )
#     log.debug( 'returning rfrnc_id for redirect, `{rfrnc_id}`' )
#     return rfrnc_id


def add_posted_relationships( data: dict, request_user_id: int, rfrnc: models_alch.Reference, session: sqlalchemy.orm.session.Session ) -> None:
    """ Creates relationship data, and implied inverse relationship data.
        Called by manage_relationships_post() """
    log.debug( 'starting add_posted_relationships()' )
    relt = models_alch.ReferentRelationship(
        subject_id=data['sbj'], role_id=data['rel'],
        object_id=data['obj'])
    session.add(relt)
    implied = relt.entailed_relationships()
    for i in implied:
        existing = session.query( models_alch.ReferentRelationship ).filter_by(
            subject_id=i.subject_id, role_id=i.role_id,
            object_id=i.object_id).first()
        if not existing:
            session.add(i)
    session.commit()
    stamp_edit( request_user_id, rfrnc, session )
    log.debug( 'relationship entry(s) created.' )
    return


def manage_relationships_delete( rltnshp_id: str, payload: bytes, request_user_id: int ) -> str:
    """ Handles ajax api call; deletes relationship entry.
        Called by views.data_relationships() 
        2023-June NOTE...
        - current implementation has empty payload. 
        - the expected payload contained an item-record-id... which is normally used to update a table of who is changing what record.
        - TODO: re-add this item-record-id to the payload.
        """
    log.debug( 'starting manage_relationships_delete()' )
    log.debug( f'rltnshp_id, ``{rltnshp_id}``' ); assert type( rltnshp_id ) == str, type(rltnshp_id)
    log.debug( f'payload, ``{payload}``' ); assert type( payload ) == bytes, type(payload)
    log.debug( f'request_user_id, ``{request_user_id}``' ); assert type( request_user_id ) == int, type(request_user_id)
    try:
        session = make_session()
        # data: dict = json.loads( payload )
        # section: int = data['section']  # seems to be the 'reference-id'
        # rfrnc = session.query( models_alch.Reference ).get( section )
        # rfrnc_id = rfrnc.id
        existing = session.query( models_alch.ReferentRelationship ).get( rltnshp_id )
        if existing:
            session.delete( existing )
            session.commit()
            session.close()
            # stamp_edit( request_user_id, rfrnc, session )
    except:
        log.exception( 'problem with delete...' )
    # log.debug( 'returning rfrnc_id for redirect, `{rfrnc_id}`' )
    # return rfrnc_id
    log.debug( 'no longer returning rfrnc_id for redirect' )
    return


# def manage_relationships_delete( rltnshp_id, payload: bytes, request_user_id: int ) -> str:
#     """ Handles ajax api call; deletes relationship entry.
#         Called by views.data_relationships() """
#     log.debug( 'starting manage_relationships_delete()' )
#     try:
#         session = make_session()
#         data: dict = json.loads( payload )
#         section: int = data['section']  # seems to be the 'reference-id'
#         rfrnc = session.query( models_alch.Reference ).get( section )
#         rfrnc_id = rfrnc.id
#         existing = session.query( models_alch.ReferentRelationship ).get( rltnshp_id )
#         if existing:
#             session.delete( existing )
#             session.commit()
#             stamp_edit( request_user_id, rfrnc, session )
#     except:
#         log.exception( 'problem with delete...' )
#     log.debug( 'returning rfrnc_id for redirect, `{rfrnc_id}`' )
#     return rfrnc_id


## common


def stamp_edit( request_user_id: int, reference_obj: models_alch.Reference, session: sqlalchemy.orm.session.Session ) -> None:
    """ Updates when the Reference-object was last edited and by whom.
        Called by manage_relationships_post() """
    log.debug( 'starting stamp_edit()' )
    edit = models_alch.ReferenceEdit( reference_id=reference_obj.id, user_id=request_user_id, timestamp=datetime.datetime.utcnow() )
    session.add( edit )
    session.commit()
    return


# -------------
# for reference
# -------------


## from DISA -- DELETE
# @app.route('/data/relationships/<relId>', methods=['DELETE'])
# @login_required
# def delete_relationship(relId):
#     log.debug( 'starting delete_relationship()' )
#     data = request.get_json()
#     ref = models.Reference.query.get(data['section'])
#     existing = models.ReferentRelationship.query.get(relId)
#     if existing:
#         db.session.delete(existing)
#         db.session.commit()
#         stamp_edit(current_user, ref)
#     return redirect(
#         url_for('relationships_by_reference', refId = ref.id),
#         code=303 )


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
