# -*- coding: utf-8 -*-

import datetime, json, logging, os, pprint

import sqlalchemy
from disa_app import models_sqlalchemy as models_alch
from disa_app import settings_app
from disa_app.lib import person_common
from django.conf import settings
from django.http import HttpResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


log = logging.getLogger(__name__)


def make_session() -> sqlalchemy.orm.session.Session:
    engine = create_engine( settings_app.DB_URL, echo=True )
    Session = sessionmaker( bind=engine )
    session = Session()
    return session


class Updater():

    def __init__( self ):
        self.session = None

    def manage_put( self, payload: bytes, request_user_id: int, rfrnt_id: str ) -> HttpResponse:
        """ Manages data/api ajax 'PUT'.
            Called by views.data_entrants(), triggered by views.edit_record() webpage. """
        log.debug( 'starting manage_put()' )
        data: dict = json.loads( payload )
        try:
            context: dict = self.execute_update( request_user_id, data, rfrnt_id )
            resp = HttpResponse( json.dumps(context, sort_keys=True, indent=2), content_type='application/json; charset=utf-8' )
        except:
            msg = 'problem preparing data'
            log.exception( msg )
            resp = HttpResponse( msg )
        log.debug( 'returning response' )
        return resp

    def execute_update( self, user_id: int, data: dict, rntId: str ) -> dict:
        """ Updates db and returns data.
            Called by manage_put() """
        self.session = make_session()
        rnt: models_sqlalchemy.Referent = self.session.query( models_alch.Referent ).get( rntId )
        primary_name: str = self.update_referent_name( data['name'] )

        rnt.names.append(primary_name)
        rnt.primary_name = primary_name


        rnt.roles = [ self.get_or_create_referent_attribute(a, models_alch.Role) for a in data['roles'] ]
        log.debug( f'rnt.roles, ```{rnt.roles}```' )

        self.session.add( rnt )
        self.session.commit()
        log.debug( 'referent add() and commit() completed' )

        self.stamp_edit( user_id, rnt.reference)

        data = {
            'name_id': rnt.primary_name.id,
            'first': rnt.primary_name.first,
            'last': rnt.primary_name.last,
            'id': rnt.id,
            'person_id': rnt.person_id,
            'roles': [ role.id for role in rnt.roles ] }

        log.debug( f'data, ```{pprint.pformat( data )}```' )
        return data

    def update_referent_name( self, data: dict ) -> models_alch.ReferentName:
        """ Obtains a ReferentName object. Does not write to the db.
            Called by execute_update() """
        log.debug( f'data, ```{data}```' )
        if data['id'] == 'name':
            name = self.session.query( models_alch.ReferentName() )
            log.debug( f'name, ```{name}```' )
        else:
            name = self.session.query( models_alch.ReferentName ).get( data['id'] )
            log.debug( f'name, ```{name}```' )
        name.first = data['first']
        name.last = data['last']
        given = self.session.query( models_alch.NameType ).filter_by( name='Given' ).first()
        log.debug( f'given, ```{given}```' )
        log.debug( f'given.id, ```{given.id}```' )
        log.debug( f'type(given.id), ```{type(given.id)}```' )
        name.name_type_id = data.get('name_type', given.id)
        log.debug( 'returning name' )
        return name

    def get_or_create_referent_attribute( self, data: dict, attrModel: models_alch.Role ) -> models_alch.Role:
        """ Obtains, or creates and obtains, and then returns, a models_alch.Role instance.
            Called by execute_update() """
        existing: models_alch.Role = self.session.query( attrModel ).filter_by( name=data['name'] ).first()  # or None, I think
        if not existing:
            new_attr: models_alch.Role = attrModel( name=data['name'] )
            self.session.add( new_attr )
            self.session.commit()
            log.debug( f'new_attr, ```{new_attr}```' )
            return new_attr
        else:
            log.debug( f'existing, ```{existing}```' )
            return existing

    def stamp_edit( self, request_user_id: int, reference_obj: models_alch.Reference ) -> None:
        """ Updates when the Reference-object was last edited and by whom.
            Called by execute_update() """
        log.debug( 'starting stamp_edit()' )
        edit = models_alch.ReferenceEdit( reference_id=reference_obj.id, user_id=request_user_id, timestamp=datetime.datetime.utcnow() )
        self.session.add( edit )
        self.session.commit()
        return

    # def stamp_edit(user, ref):
    #     edit = models.ReferenceEdit(reference_id=ref.id,
    #         user_id=user.id, timestamp=datetime.datetime.utcnow())
    #     db.session.add(edit)
    #     db.session.commit()

    ## end class Updater()


## from DISA
# @app.route('/data/entrants/', methods=['POST'])
# @app.route('/data/entrants/<rntId>', methods=['PUT', 'DELETE'])
# @login_required
# def update_referent(rntId=None):
#     if request.method == 'DELETE':
#         rnt = models.Referent.query.get(rntId)
#         ref = rnt.reference
#         rels_as_sbj = models.ReferentRelationship.query.filter_by(
#             subject_id=rnt.id).all()
#         rels_as_obj = models.ReferentRelationship.query.filter_by(
#             object_id=rnt.id).all()
#         for r in rels_as_sbj:
#             db.session.delete(r)
#         for r in rels_as_obj:
#             db.session.delete(r)
#         db.session.delete(rnt)
#         db.session.commit()

#         stamp_edit(current_user, ref)

#         return jsonify( { 'id': rntId } )
#     data = request.get_json()
#     if request.method == 'POST':
#         prs = models.Person()
#         db.session.add(prs)
#         db.session.commit()
#         rnt = models.Referent(reference_id=data['record_id'])
#         rnt.person = prs
#     if request.method == 'PUT':
#         rnt = models.Referent.query.get(rntId)
#     primary_name = update_referent_name(data['name'])
#     rnt.names.append(primary_name)
#     rnt.primary_name = primary_name
#     if request.method == 'POST':
#         prs.first_name = primary_name.first
#         prs.last_name = primary_name.last
#         db.session.add(prs)
#     rnt.roles = [ get_or_create_referent_attribute(a, models.Role)
#         for a in data['roles'] ]
#     db.session.add(rnt)
#     db.session.commit()

#     stamp_edit(current_user, rnt.reference)

#     return jsonify({
#         'name_id': rnt.primary_name.id,
#         'first': rnt.primary_name.first,
#         'last': rnt.primary_name.last,
#         'id': rnt.id,
#         'person_id': rnt.person_id,
#         'roles': [ role.id for role in rnt.roles ] })
