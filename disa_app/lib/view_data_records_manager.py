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


def query_record( rec_id ):
    data = { 'rec': {}, 'entrants': [] }
    if rec_id == None:
        data = json.dumps( data )
    else:
        session = make_session()
    log.debug( f'data, ```{pprint.pformat(data)}```' )
    1/0
    return data


## from DISA
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
