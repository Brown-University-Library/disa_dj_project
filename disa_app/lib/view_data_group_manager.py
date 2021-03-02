import datetime, json, logging, os, pprint, uuid

import sqlalchemy
from disa_app import models_sqlalchemy as models_alch
from disa_app import settings_app
# from disa_app.lib import person_common
from django.conf import settings
from django.core.urlresolvers import reverse
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
        """ Manages data/api ajax 'GET'.
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
