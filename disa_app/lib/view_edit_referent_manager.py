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

def prep_context( rfrnt_id: str, usr_first_name: str, usr_is_authenticated: bool ) -> dict:
    """ Builds context for edit-referent display.
        Called by views.edit_person() """
    context = { 'user_first_name': usr_first_name, 'user_is_authenticated': usr_is_authenticated }
    session = make_session()
    log.debug( 'context prepared' )
    return context




## from DISA
# @app.route('/editor/person')
# @app.route('/editor/person/<entId>')
# @login_required
# def edit_entrant(entId=None):
#     log.debug( 'starting edit_entrant' )
#     nametypes = [ { 'id': role.id, 'value': role.name, 'label': role.name }
#         for role in models.NameType.query.all()]
#     roles = [ { 'id': role.id, 'value': role.name, 'label': role.name }
#         for role in models.Role.query.all()]
#     # desc_data = models.Description.query.all()
#     origins = [ { 'id': loc.name, 'value': loc.name, 'label': loc.name }
#         for loc in models.Location.query.all()]
#     races = [ { 'id': loc.name, 'value': loc.name, 'label': loc.name }
#         for loc in models.Race.query.all()]
#     tribes = [ { 'id': loc.name, 'value': loc.name, 'label': loc.name }
#         for loc in models.Tribe.query.all()]
#     titles = [ { 'id': loc.name, 'value': loc.name, 'label': loc.name }
#         for loc in models.Title.query.all()]
#     vocations = [ { 'id': loc.name, 'value': loc.name, 'label': loc.name }
#         for loc in models.Vocation.query.all()]
#     enslavements = [ { 'id': loc.name, 'value': loc.name, 'label': loc.name }
#         for loc in models.EnslavementType.query.all()]
#     if not entId:
#         rec_id = request.args.get('rec')
#         rec = models.Reference.query.get(rec_id)
#         return render_template(
#             'entrant_edit.html', roles=roles, rec=rec, ent=None)
#     ent = models.Referent.query.get(entId)
#     return render_template(
#         'entrant_edit.html', rec=ent.reference, ent=ent,
#         nametypes=nametypes,
#         roles=roles, origins=origins, races=races, tribes=tribes,
#         vocations=vocations, enslavements=enslavements,
#         titles=titles)
