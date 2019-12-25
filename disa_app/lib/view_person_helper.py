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


def query_person( prsn_id ):
    """ Queries db for person.
        Called by views.person()
        """
    log.debug( 'starting query_person()' )
    session = make_session()
    prsn: models_sqlalchemy.Person = session.query( models_alch.Person ).get( prsn_id )
    log.debug( f'prsn, ```{prsn}```' )
    prsn_info = {
        'name': person_common.parse_person_name( prsn ),
        'tribes': person_common.parse_person_descriptors( prsn, 'tribes' ),
        'origins': person_common.parse_person_descriptors( prsn, 'origins' ),
        'races': person_common.parse_person_descriptors( prsn, 'races' ),
        'statuses': person_common.parse_person_descriptors( prsn, 'enslavements' ),
        'vocations': person_common.parse_person_descriptors( prsn, 'vocations' ),

        'dbId': prsn.id
        }
    return prsn_info


## from DISA
# @app.route('/people/<persId>')
# def get_person(persId):
#     log.debug( 'starting get_person' )
#     person = models.Person.query.get(persId)
#     name = parse_person_name(person)
#     tribes = parse_person_descriptors(person, 'tribes')
#     origins = parse_person_descriptors(person, 'origins')
#     races = parse_person_descriptors(person, 'races')
#     statuses = parse_person_descriptors(person, 'enslavements')
#     vocations = parse_person_descriptors(person, 'vocations')
#     titles = parse_person_descriptors(person, 'titles')
#     relations = parse_person_relations(person)
#     return render_template('person_display.html',
#         name=name, dbId=persId, refs = person.references,
#         origins=origins, tribes=tribes, titles=titles,
#         races=races, vocations=vocations, statuses=statuses,
#         relations=relations)
