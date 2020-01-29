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


# -------------
# main
# -------------

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
    log.debug( f'data, ```{pprint.pformat(data)}```' )
    try:  # for debugging; remove afterwards
        reference_type: models_sqlalchemy.ReferenceType = get_or_create_type( data['record_type'], models_alch.ReferenceType, session )

        rfrnc = models_alch.Reference()
        rfrnc.citation_id = data['citation_id']
        rfrnc.national_context_id = data['national_context']
        rfrnc.reference_type_id = reference_type.id
        session.add( rfrnc )
        session.commit()

        rfrnc.locations = []
        rfrnc = process_record_locations( data['locations'], rfrnc, session )

    except:
        log.exception( '\n\nexception...' )

    return


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


# -------------
# helpers
# -------------


def make_session() -> sqlalchemy.orm.session.Session:
    engine = create_engine( settings_app.DB_URL, echo=True )
    Session = sessionmaker( bind=engine )
    session = Session()
    return session


def get_or_create_type( typeData: dict, typeModel: models_alch.ReferenceType, session: sqlalchemy.orm.session.Session ) -> models_alch.ReferenceType:
    """ Gets or creates a ReferenceType instance.
        Called by manage_post() """
    log.debug( f'typeData, ```{pprint.pformat(typeData)}```' )
    if typeData['id'] == -1:
        new_type = typeModel (name=typeData['value'] )
        session.add( new_type )
        session.commit()
        log.debug( f'new_type, ```{new_type}```' )
        typ = new_type
    elif typeData == '' or typeData['id'] == 0:
        unspec = session.query( typeModel ).filter_by( name='Unspecified' ).first()
        log.debug( f'unspec, ```{unspec}```' )
        typ = unspec
    else:
        existing = session.query( typeModel ).get( typeData['id'] )
        log.debug( f'existing, ```{existing}```' )
        typ = existing
    return typ


def process_record_locations( locData: list, recObj: models_alch.Reference, session: sqlalchemy.orm.session.Session ) -> models_alch.Reference:
    """ Creates additional Location records if necessary...
        Updates ReferenceLocation records if necessary...
        Creates a linkage between the Reference record and the ReferenceLocation record if necessary.
        Called by manage_post() """
    log.debug( f'locData, ```{pprint.pformat(locData)}```' )
    locations = []
    for loc in locData:
        if loc['id'] == -1:
            location = models.Location(name=loc['value'])
            db.session.add(location)
            db.session.commit()
        elif loc['id'] == 0:
            continue
        else:
            location = models.Location.query.get(loc['id'])
        locations.append(location)
    # clny_state = models.LocationType.query.filter_by(name='Colony/State').first()
    clny_state = session.query( models_alch.LocationType ).filter_by( name='Colony/State' ).first()

    # city = models.LocationType.query.filter_by(name='City').first()
    city = session.query( models_alch.LocationType ).filter_by( name='City' ).first()

    # locale = models.LocationType.query.filter_by(name='Locale').first()
    locale = session.query( models_alch.LocationType ).filter_by( name='Locale' ).first()

    loc_types = [ clny_state, city, locale ]
    for loc in locations:
        rec_loc = models_alch.ReferenceLocation()
        rec_loc.reference = recObj
        rec_loc.location = loc
        idx = locations.index( loc )
        rec_loc.location_rank = idx
        if idx < len(loc_types):
            rec_loc.location_type = loc_types[idx]
        session.add(rec_loc)
    session.commit()
    log.debug( 'returning reference-instance' )
    return recObj


# def process_record_locations(locData, recObj):
#     locations = []
#     for loc in locData:
#         if loc['id'] == -1:
#             location = models.Location(name=loc['value'])
#             db.session.add(location)
#             db.session.commit()
#         elif loc['id'] == 0:
#             continue
#         else:
#             location = models.Location.query.get(loc['id'])
#         locations.append(location)
#     clny_state = models.LocationType.query.filter_by(name='Colony/State').first()
#     city = models.LocationType.query.filter_by(name='City').first()
#     locale = models.LocationType.query.filter_by(name='Locale').first()
#     loc_types = [ clny_state, city, locale ]
#     for loc in locations:
#         rec_loc = models.ReferenceLocation()
#         rec_loc.reference = recObj
#         rec_loc.location = loc
#         idx = locations.index(loc)
#         rec_loc.location_rank = idx
#         if idx < len(loc_types):
#             rec_loc.location_type = loc_types[idx]
#         db.session.add(rec_loc)
#     db.session.commit()
#     return recObj


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
