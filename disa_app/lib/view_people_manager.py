# -*- coding: utf-8 -*-

import datetime, json, logging, os, pprint

from disa_app import settings_app
from disa_app import models_sqlalchemy as models_alch
from django.conf import settings

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


log = logging.getLogger(__name__)


def make_session():
    engine = create_engine( settings_app.DB_URL, echo=True )
    Session = sessionmaker( bind=engine )
    session = Session()
    return session


def query_people():
    """ Queries db for people.
        Called by views.people()
        Resources:
        - <https://stackoverflow.com/questions/19406859/sqlalchemy-convert-select-query-result-to-a-list-of-dicts/20078977>
        - <https://stackoverflow.com/questions/2828248/sqlalchemy-returns-tuple-not-dictionary>
        """
    log.debug( 'starting query_people()' )
    session = make_session()
    resultset: List(sqlalchemy.util._collections.result) = session.query(
        models_alch.Person, models_alch.Referent ).filter( models_alch.Person.id == models_alch.Referent.id ).all()
    log.debug( f'type(resultset), `{type(resultset)}`' )
    log.debug( f'resultset[0], ```{resultset[0]}```' )
    people = []
    for ( prsn, rfrnt ) in resultset:
        entry = { 'db_id': prsn.id }
        entry['db_sex'] = rfrnt.sex
        entry['calc_sex'] = rfrnt.sex if rfrnt.sex else 'Not Listed'
        entry['db_age'] = rfrnt.age
        entry['calc_age'] = rfrnt.age if rfrnt.age else 'Not Listed'
        prep_race( entry, rfrnt )
        prep_status( entry, rfrnt )
        prep_name( entry, prsn )
        people.append( entry )
    log.debug( f'people (first 3), ```{pprint.pformat(people[0:3])}```...' )
    return people


def prep_race( entry: dict, rfrnt: models_alch.Referent ) -> None:
    """ Updates entry with race data.
        Called by query_people() """
    db_race = []
    calc_race = ''
    if len( rfrnt.races ) > 0:  # rfrnt.races: sqlalchemy.orm.collections.InstrumentedList
        db_race: str = rfrnt.races[0].name  # there is only ever one Race associated-record
        calc_race: str = db_race
    else:
        calc_race = 'Not Listed'
    entry['db_race'] = db_race
    entry['calc_race'] = calc_race
    return


def prep_status( entry: dict, rfrnt: models_alch.Referent ) -> None:
    """ Updates entry with enslavement-type/status data.
        Called by query_people() """
    db_status = []
    calc_status = ''
    if len( rfrnt.enslavements ) > 0:  # rfrnt.enslavements: sqlalchemy.orm.collections.InstrumentedList
        db_status: str = rfrnt.enslavements[0].name  # there is only ever one EnslavementType associated-record
        calc_status: str = db_status
    else:
        calc_status = 'Not Listed'
    entry['db_status'] = db_status
    entry['calc_status'] = calc_status
    return


def prep_name( entry: dict, prsn: models_alch.Person ) -> None:
    """ Updates entry with name data.
        Called by query_people() """
    entry['db_name_first'] = prsn.first_name  # first_name: str
    entry['db_name_last'] = prsn.last_name  # last_name: str
    calc_name: str = f'{prsn.first_name} {prsn.last_name}'.strip()
    calc_name: str = calc_name if calc_name else 'Not Listed'
    entry['calc_name'] = calc_name


# db = SQLAlchemy(app)
# db_url = settings_app.DB_URL
# people = []
# for (prsn, rfrnt) in db.session.query( models.Person, models.Referent ).filter( models.Person.id==models.Referent.id ).all():
#     sex = rfrnt.sex if rfrnt.sex else 'Not Listed'
#     age = rfrnt.age if rfrnt.age else 'Not Listed'
#     race = None
#     try:
#         race = rfrnt.races[0].name
#     except:
#         log.debug( 'no race-name; races, ```{rfrnt.races}```' )
#     race = race if race else 'Not Listed'
#     temp_demographic = f'age, `{age}`; sex, `{sex}`; race, `{race}`'
#     # prsn.tmp_dmgrphc = temp_demographic
#     # prsn.last_name = f'{prsn.last_name} ({temp_str})'
#     prsn.calc_sex = sex
#     prsn.calc_age = age
#     prsn.calc_race = race
#     people.append( prsn )
# p = people[1]
# log.debug( f'p.__dict__, ```{p.__dict__}```' )
