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


def query_record( rec_id: str ) -> dict:
    """ Handles api call for GET reference-data and associated referent-data.
        Called by views.data_records() """
    data = { 'rec': {}, 'entrants': [] }
    if rec_id == None:
        data = json.dumps( data )
        log.debug( f'no rec_id; data, ```{pprint.pformat(data)}```' )
    session = make_session()
    rec: models_sqlalchemy.Reference = session.query( models_alch.Reference ).get( rec_id )
    data['rec']['id'] = rec.id
    data['rec']['date'] = None
    if rec.date:
        data['rec']['date'] = '{}/{}/{}'.format(rec.date.month,
            rec.date.day, rec.date.year)
    data['rec']['locations'] = [ {
        'label':l.location.name,
        'value':l.location.name,
        'id': l.location.id } for l in rec.locations ]
    data['rec']['transcription'] = rec.transcription
    data['rec']['national_context'] = rec.national_context_id
    data['rec']['record_type'] = {
        'label': rec.reference_type.name,
        'value': rec.reference_type.name,
        'id':rec.reference_type.id }
    data['entrants'] = [ {
        'name_id': ent.primary_name.id,
        'first': ent.primary_name.first,
        'last': ent.primary_name.last,
        'id': ent.id,
        'person_id': ent.person_id,
        'roles': [ role.id for role in ent.roles ] } for ent in rec.referents ]
    data['rec']['header'] = '{}'.format(
        rec.reference_type.name or '').strip()

    log.debug( f'data, ```{pprint.pformat(data)}```' )
    return data


def manage_post( payload: bytes, request_user_id: int ) -> dict:
    """ Handles api call when 'Create' button is hit in `/editor/records/?doc_id=123`.
        Called by views.data_records() """
    log.debug( 'starting manage_relationships_post()' )
    session = make_session()
    data: dict = json.loads( payload )

    reference_type = get_or_create_type(
        data['record_type'], models.ReferenceType)


## helpers


def get_or_create_type( typeData, typeModel ):
    if typeData['id'] == -1:
        new_type = typeModel(name=typeData['value'])
        db.session.add(new_type)
        db.session.commit()
        return new_type
    elif typeData == '' or typeData['id'] == 0:
        unspec = typeModel.query.filter_by(name='Unspecified').first()
        return unspec
    else:
        existing = typeModel.query.get(typeData['id'])
        return existing


# -------------
# for reference
# -------------


## from DISA -- POST/PUT
# @app.route('/data/records/', methods=['POST'])
# @app.route('/data/records/<refId>', methods=['PUT'])
# @login_required
# def update_reference_data(refId=None):
#     data = request.get_json()
#     reference_type = get_or_create_type(
#         data['record_type'], models.ReferenceType)
#     if request.method == 'POST':
#         ref = models.Reference()
#         ref.citation_id = data['citation_id']
#         ref.national_context_id = data['national_context']
#         ref.reference_type_id = reference_type.id
#         db.session.add(ref)
#         db.session.commit()
#     else:
#         ref = models.Reference.query.get(refId)
#     ref.locations = []
#     ref = process_record_locations(data['locations'], ref)
#     try:
#         ref.date = datetime.datetime.strptime(data['date'], '%m/%d/%Y')
#     except:
#         ref.date = None
#     ref.reference_type_id = reference_type.id
#     ref.national_context_id = data['national_context']
#     ref.transcription = data['transcription']
#     db.session.add(ref)
#     db.session.commit()

#     stamp_edit(current_user, ref)
#     if request.method == 'POST':
#         return jsonify(
#             { 'redirect': url_for('edit_record', recId=ref.id) })
#     data = { 'rec': {} }
#     data['rec']['id'] = ref.id
#     data['rec']['date'] = ''
#     if ref.date:
#         data['rec']['date'] = '{}/{}/{}'.format(ref.date.month,
#             ref.date.day, ref.date.year)
#     if request.method == 'POST':
#         data['entrants'] = []
#         data['rec']['header'] = '{}'.format(
#             ref.reference_type.name or '').strip()
#     data['rec']['citation'] = ref.citation.id
#     data['rec']['transcription'] = ref.transcription
#     data['rec']['national_context'] = ref.national_context_id
#     data['rec']['locations'] = [
#         { 'label':l.location.name, 'value':l.location.name,
#             'id': l.location.id } for l in ref.locations ]
#     data['rec']['record_type'] = {'label': ref.reference_type.name,
#         'value': ref.reference_type.name, 'id':ref.reference_type.id }
#     return jsonify(data)


## from DISA -- GET
# @app.route('/data/records/', methods=['GET'])
# @app.route('/data/records/<recId>', methods=['GET'])
# @login_required
# def read_record_data(recId=None):
#     data = { 'rec': {}, 'entrants': [] }
#     if recId == None:
#         return jsonify(data)
#     rec = models.Reference.query.get(recId)
#     data['rec']['id'] = rec.id
#     data['rec']['date'] = None
#     if rec.date:
#         data['rec']['date'] = '{}/{}/{}'.format(rec.date.month,
#             rec.date.day, rec.date.year)
#     data['rec']['locations'] = [
#         { 'label':l.location.name, 'value':l.location.name,
#             'id': l.location.id } for l in rec.locations ]
#     data['rec']['transcription'] = rec.transcription
#     data['rec']['national_context'] = rec.national_context_id
#     data['rec']['record_type'] = {'label': rec.reference_type.name,
#         'value': rec.reference_type.name, 'id':rec.reference_type.id }
#     data['entrants'] = [
#         {
#             'name_id': ent.primary_name.id,
#             'first': ent.primary_name.first,
#             'last': ent.primary_name.last,
#             'id': ent.id,
#             'person_id': ent.person_id,
#             'roles': [ role.id for role in ent.roles ]
#         }
#             for ent in rec.referents ]
#     data['rec']['header'] = '{}'.format(
#         rec.reference_type.name or '').strip()
#     return jsonify(data)
