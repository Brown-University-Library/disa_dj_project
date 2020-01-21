# -*- coding: utf-8 -*-

import datetime, json, logging, os, pprint

import django, sqlalchemy
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


def prep_context( rec_id: str, usr_first_name: str, usr_is_authenticated: bool ) -> dict:
    """ Queries and massages data.
        Called by views.edit_relationships() """
    context = { 'user_first_name': usr_first_name, 'user_is_authenticated': usr_is_authenticated }
    session = make_session()

    rec = session.query( models_alch.Reference ).get( rec_id )

    context['reference'] = rec.dictify()

    log.debug( f'context, ```{pprint.pformat(context)}```' )
    return context




## from DISA
# @app.route('/record/relationships/<recId>')
# @login_required
# def edit_relationships(recId):
#     log.debug( 'starting edit_relationships' )
#     log.debug( 'request.__dict__, ```%s```' % pprint.pformat(request.__dict__) )
#     rec = models.Reference.query.get(recId)
#     # return render_template('record_relationships.html', sec=rec)
#     base_segment = request.script_root
#     return render_template('record_relationships.html', sec=rec, base_url_segment=base_segment )
