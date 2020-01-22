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


class Getter():
    def __init__( self ):
        self.session = None

    def manage_get( self, rfrnt_id: str ) -> HttpResponse:
        """ Manages data/api ajax 'PUT'.
            Called by views.data_entrants(), triggered by views.edit_person() webpage. """
        log.debug( 'starting manage_get' )
        log.debug( f'rfrnt_id, ```{rfrnt_id}```' )
        self.session = make_session()
        try:
            rfrnt: models_sqlalchemy.Referent = self.session.query( models_alch.Referent ).get( rfrnt_id )
            context: dict = self.prep_get_response( rfrnt )
            resp = HttpResponse( json.dumps(context, sort_keys=True, indent=2), content_type='application/json; charset=utf-8' )
        except:
            msg = 'problem with update, or with response-prep; see logs'
            log.exception( msg )
            resp = HttpResponse( msg )
        log.debug( 'returning response' )
        return resp

    def prep_get_response( self, rfrnt: models_alch.Referent ) -> dict:
        """ Prepares context.
            Called by manage_get() """
        data = { 'ent': {} }
        data['ent']['id'] = rfrnt.id
        data['ent']['names'] = [
            { 'first': n.first, 'last': n.last,
                'name_type': n.name_type.name,
                'id': n.id } for n in rfrnt.names ]
        data['ent']['age'] = rfrnt.age
        data['ent']['sex'] = rfrnt.sex
        data['ent']['races'] = [
            { 'label': r.name, 'value': r.name,
                'id': r.name } for r in rfrnt.races ]
        data['ent']['tribes'] = [
            { 'label': t.name, 'value': t.name,
                'id': t.name } for t in rfrnt.tribes ]
        data['ent']['origins'] = [
            { 'label': o.name, 'value': o.name,
                'id': o.name } for o in rfrnt.origins ]
        data['ent']['titles'] = [
            { 'label': t.name, 'value': t.name,
                'id': t.name } for t in rfrnt.titles ]
        data['ent']['vocations'] = [
            { 'label': v.name, 'value': v.name,
                'id': v.name } for v in rfrnt.vocations ]
        data['ent']['enslavements'] = [
            { 'label': e.name, 'value': e.name,
                'id': e.name } for e in rfrnt.enslavements ]
        log.debug( f'data, ```{pprint.pformat(data)}```' )
        return data

    ## end class Getter()


class Updater():

    def __init__( self ):
        self.session = None

    def manage_put( self, payload: bytes, request_user_id: int, rfrnt_id: str ) -> HttpResponse:
        """ Manages data/api ajax 'PUT'.
            Called by views.data_entrants(), triggered by views.edit_record() webpage. """
        log.debug( 'starting manage_put()' )
        self.session = make_session()
        data: dict = json.loads( payload )
        try:
            context: dict = self.execute_update( request_user_id, data, rfrnt_id )
            resp = HttpResponse( json.dumps(context, sort_keys=True, indent=2), content_type='application/json; charset=utf-8' )
        except:
            msg = 'problem with update, or with response-prep; see logs'
            log.exception( msg )
            resp = HttpResponse( msg )
        log.debug( 'returning response' )
        return resp

    def execute_update( self, user_id: int, data: dict, rntId: str ) -> dict:
        """ Updates db and returns data.
            Called by manage_put() """
        rnt: models_sqlalchemy.Referent = self.session.query( models_alch.Referent ).get( rntId )
        primary_name: str = self.update_referent_name( data['name'] )
        rnt.names.append( primary_name )
        rnt.primary_name = primary_name
        rnt.roles = [ self.get_or_create_referent_attribute(a, models_alch.Role) for a in data['roles'] ]
        self.session.add( rnt )
        self.session.commit()
        self.stamp_edit( user_id, rnt.reference)
        data = self.prep_response_data( rnt )
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
        name.name_type_id: int = data.get('name_type', given.id)
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

    def prep_response_data( self, referent: models_alch.Referent ) -> dict:
        """ Prepares dct for json response.
            Called by execute_update() """
        data = {
            'name_id': referent.primary_name.id,
            'first': referent.primary_name.first,
            'last': referent.primary_name.last,
            'id': referent.id,
            'person_id': referent.person_id,
            'roles': [ role.id for role in referent.roles ]
            }
        log.debug( f'data, ```{pprint.pformat( data )}```' )
        return data

    ## end class Updater()


class Poster():
    def __init__( self ):
        self.session = None

    def manage_post( self, rfrnt_id: str ) -> HttpResponse:
        """ Manages data/api ajax 'POST'.
            Called by views.data_entrants(), triggered by views.edit_record() webpage 'Add person' button save. """
        log.debug( 'starting manage_post' )
        self.session = make_session()
        # try:
        #     rfrnt: models_sqlalchemy.Referent = self.session.query( models_alch.Referent ).get( rfrnt_id )
        #     context: dict = self.prep_get_response( rfrnt )
        #     resp = HttpResponse( json.dumps(context, sort_keys=True, indent=2), content_type='application/json; charset=utf-8' )
        # except:
        #     msg = 'problem with update, or with response-prep; see logs'
        #     log.exception( msg )
        #     resp = HttpResponse( msg )
        log.debug( 'returning response' )
        return HttpResponse( 'post-handling coming' )



## from DISA -- GET
# @app.route('/data/entrants/', methods=['GET'])
# @app.route('/data/entrants/<rntId>', methods=['GET'])
# @login_required
# def read_referent_data(rntId=None):
#     data = { 'ent': {} }
#     if rntId == None:
#         return jsonify(data)
#     rnt = models.Referent.query.get(rntId)
#     data['ent']['id'] = rnt.id
#     data['ent']['names'] = [
#         { 'first': n.first, 'last': n.last,
#             'name_type': n.name_type.name,
#             'id': n.id } for n in rnt.names ]
#     data['ent']['age'] = rnt.age
#     data['ent']['sex'] = rnt.sex
#     data['ent']['races'] = [
#         { 'label': r.name, 'value': r.name,
#             'id': r.name } for r in rnt.races ]
#     data['ent']['tribes'] = [
#         { 'label': t.name, 'value': t.name,
#             'id': t.name } for t in rnt.tribes ]
#     data['ent']['origins'] = [
#         { 'label': o.name, 'value': o.name,
#             'id': o.name } for o in rnt.origins ]
#     data['ent']['titles'] = [
#         { 'label': t.name, 'value': t.name,
#             'id': t.name } for t in rnt.titles ]
#     data['ent']['vocations'] = [
#         { 'label': v.name, 'value': v.name,
#             'id': v.name } for v in rnt.vocations ]
#     data['ent']['enslavements'] = [
#         { 'label': e.name, 'value': e.name,
#             'id': e.name } for e in rnt.enslavements ]
#     return jsonify(data)


## from DISA -- PUT
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
