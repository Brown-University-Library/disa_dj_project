# -*- coding: utf-8 -*-

import datetime, json, logging, os, pprint

import django, sqlalchemy
from disa_app import settings_app
from disa_app import models_sqlalchemy as models_alch
from disa_app.lib import person_common
from django.conf import settings
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker


log = logging.getLogger(__name__)


def make_session() -> sqlalchemy.orm.session.Session:
    engine = create_engine( settings_app.DB_URL, echo=True )
    Session = sessionmaker( bind=engine )
    session = Session()
    return session


# def run_search( srch_text: str ) -> dict:
#     session = make_session()
#     data = {}
#     log.debug( f'srch_text, ```{srch_text}```' )


def experiment():
    session = make_session()

    qset_people = session.query( models_alch.Person ).filter(
        or_(
            models_alch.Person.first_name.contains('Ming'),
            models_alch.Person.last_name.contains('Ming')
            ) ).all()
    print( '\n\n---\n\nPeople...' )
    for x in qset_people:
        print( f'\n\n---\n\n```{pprint.pformat(x.__dict__)}```' )

    qset_citations = session.query( models_alch.Citation ).filter(
        or_(
            models_alch.Citation.display.contains('Ming'),
            models_alch.Citation.comments.contains('Ming')
            ) ).all()
    print( '\n\n---\n\nCitations...' )
    for x in qset_citations:
        print( f'\n\n---\n\n```{pprint.pformat(x.__dict__)}```' )

    qset_items = session.query( models_alch.Reference ).filter(
        or_(
            models_alch.Reference.transcription.contains('Ming')
            ) ).all()
    print( '\n\n---\n\nItems...' )
    for x in qset_items:
        print( f'\n\n---\n\n```{pprint.pformat(x.__dict__)}```' )


experiment()
