# -*- coding: utf-8 -*-

import datetime, json, logging, os, pprint

from disa_app import settings_app
# from disa_app.models_sqlalchemy import Person, Referent
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

        race = None
        log.debug( f'rfrnt.races, ```{rfrnt.races}```' )
        try:
            race = rfrnt.races[0].name
            log.debug( f'race, `{race}`' )
        except:
            log.debug( f'no race-name; races, ```{rfrnt.races}```' )
        race = race if race else 'Not Listed'
        log.debug( f'rfrnt.enslavements, ```{rfrnt.enslavements}```' )
        calc_status = ''
        try:
            statuses: sqlalchemy.orm.collections.InstrumentedList = rfrnt.enslavements
            status: EnslavementType = statuses[0]  # there is only ever one enslavement-type
            calc_status: str = status.name
            log.debug( f'type(statuses), ```{type(statuses)}```' )
            log.debug( f'type(statuses[0]), ```{type(statuses[0])}```' )
            log.debug( f'len(statuses), `{len(statuses)}`' )
            log.debug( f'statuses[0].name, ```{statuses[0].name}```' )
        except IndexError:
            log.debug( 'no enslavements result' )
            pass
        except:
            log.exception( 'problem ascertaining rfrnt.enslavements; traceback follows; processing will continue' )
            pass
        calc_name = f'{prsn.first_name} {prsn.last_name}'.strip()
        if not calc_name:
            calc_name = 'Not Listed'
        entry['calc_name'] = calc_name
        entry['calc_age'] = age
        # entry['calc_sex'] = sex
        entry['calc_race'] = race
        entry['calc_status'] = calc_status
        people.append( entry )
    log.debug( f'people, ```{pprint.pformat(people)}```' )
    return people


def prep_race( entry: dict, rfrnt ) -> None:
    """ Updates entry.
        Called by query_people() """
    log.debug( f'type(rfrnt), ```{}```' )
    db_race = []
    calc_race = ''
    if len( rfrnt.races ) > 0:  # rfrnt.races: List(Race)
        db_race: str = db_race[0].name
    else:
        calc_race = 'Not Listed'
    entry['db_race'] = db_race
    entry['calc_race'] = calc_race
    return



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

