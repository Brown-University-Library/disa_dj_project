import datetime, json, logging, pprint, uuid
from urllib.parse import urlparse
        

import sqlalchemy
from disa_app import models_sqlalchemy as models_alch
from disa_app import settings_app
from django.core.urlresolvers import reverse
from sqlalchemy import orm
from sqlalchemy import or_


log = logging.getLogger(__name__)


## CREATE -----------------------------------------------------------

def manage_post( request_body: str, request_url: str, start_time: datetime.datetime ) -> dict:
    """ Manages referent-match creation.
        Returns context.
        Called by tests, and views.data_referent_match() """
    try:
        log.debug( f'request_body, ``{request_body}``' )
        log.debug( f'request_url, ``{request_url}``' ) 
        context = {}
        ## extract data from post payload ---------------------------
        post_data: dict = json.loads( request_body )
        log.debug( f'post_data, ``{pprint.pformat(post_data)}``' )
        rfrnt_sbj_uuid: str = post_data['rfrnt_sbj_uuid']
        rfrnt_obj_uuid: str = post_data['rfrnt_obj_uuid']
        researcher_notes: str = post_data['researcher_notes']
        confidence: int = post_data['confidence']
        uid: str = uuid.uuid4().hex
        ## see if entry already exists ------------------------------
        session_instance = make_session()
        duplicate_check_1: list = session_instance.query( models_alch.ReferentMatch ).filter( 
            models_alch.ReferentMatch.referent_sbj_uuid == rfrnt_sbj_uuid).filter(
            models_alch.ReferentMatch.referent_obj_uuid == rfrnt_obj_uuid ).all()
        if len( duplicate_check_1 ) > 0:
            log.warning( 'duplicate found in first check; returning `400`' )
            context = { '400': 'Bad Request; match already exists'}
            return context            
        duplicate_check_2: list = session_instance.query( models_alch.ReferentMatch ).filter( 
                models_alch.ReferentMatch.referent_sbj_uuid == rfrnt_obj_uuid).filter(
                models_alch.ReferentMatch.referent_obj_uuid == rfrnt_sbj_uuid ).all()
        if len( duplicate_check_2 ) > 0:
            log.warning( 'duplicate found in second check; returning `400`' )
            context = { '400': 'Bad Request; match already exists'}
            return context
        log.debug( 'no duplicates found; will create new entry' )
        ## create new entry -----------------------------------------
        match = models_alch.ReferentMatch()
        match.uuid = uid
        match.referent_sbj_uuid = rfrnt_sbj_uuid
        match.referent_obj_uuid = rfrnt_obj_uuid
        match.confidence = confidence
        match.researcher_notes = researcher_notes
        match.date_created = datetime.datetime.now()
        match.date_edited = datetime.datetime.now()
        ## save it --------------------------------------------------
        session_instance.add( match )
        session_instance.commit()  # returns None, so no way to verify success
        ## prepare response -----------------------------------------
        response_dct: dict = prepare_common_response_dct( match, start_time )
        context = {
            'request': {
                'url': request_url,
                'method': 'POST',
                'payload': post_data,
                'timestamp': str( start_time )
            },
            'response': response_dct
        }
    except Exception as e:
        log.error( f'e, ``{repr(e)}``')
        msg = 'problem with creation, or with response-prep; see logs'
        log.exception( msg )
        context = { '500': msg }
    log.debug( f'context, ``{context}``' )
    return context

    ## end def manage_post()


## READ -------------------------------------------------------------


def manage_get_meta( request_url: str, start_time: datetime.datetime ):
    return {}


def manage_get_all( request_url: str, start_time: datetime.datetime ):
    """ Manages referent-match get for all matches.
        Returns context.
        Called by tests, and views.data_referent_match() """
    log.debug( f'request_url, ``{request_url}``' )
    try:
        context = {
            'request': {
                'url': request_url,
                'method': 'GET',
                'timestamp': str( start_time )
            },
            'response': {
                'meta': {},
                'relationship_matches': [],
            }
        }
        session_instance = make_session()
        resultset = session_instance.query( models_alch.ReferentMatch )
        # log.debug( f'type(resultset), ``{type(resultset)}``' )
        matches = []
        url_parts = urlparse( request_url )
        relationship_match_pattern = reverse( 'data_referent_match_url', kwargs={'incoming_identifier': 'FOO'} )
        referent_match_pattern = reverse( 'data_referent_url', kwargs={'rfrnt_id': 'BAR'} )
        for entry in resultset:
            relationship_match_pattern = relationship_match_pattern.replace( 'FOO', entry.uuid )
            relationship_uuid_url = '%s://%s%s' % ( url_parts.scheme, url_parts.netloc, relationship_match_pattern )
            subject_match_pattern = referent_match_pattern.replace( 'BAR', f'uuid/{entry.referent_sbj_uuid}' )
            subject_url = '(coming-soon)%s://%s%s' % ( url_parts.scheme, url_parts.netloc, subject_match_pattern )
            object_match_pattern = referent_match_pattern.replace( 'BAR', f'uuid/{entry.referent_obj_uuid}' )
            object_url = '(coming-soon)%s://%s%s' % ( url_parts.scheme, url_parts.netloc, object_match_pattern )
            dct = {
                'relationship_uuid': entry.uuid,
                'relationship_uuid_url': relationship_uuid_url,
                'referent_subject_uuid': entry.referent_sbj_uuid,
                'referent_subject_url': subject_url,
                'referent_object_uuid': entry.referent_obj_uuid,
                'referent_object_url': object_url,
                'researcher_notes': entry.researcher_notes,
                'confidence': entry.confidence
            }
            matches.append( dct )
        context['response']['relationship_matches'] = matches
        # log.debug( f'type(resulset.count), ``{type(resultset.count())}``' )
        context['response']['meta'] = { 'count': resultset.count() }
    except Exception as e:
        log.error( f'e, ``{repr(e)}``')
        msg = 'problem with get all, or with its response-prep; see logs'
        log.exception( msg )
        context = { '500': msg }
    log.debug( f'context, ``{context}``' )
    return context


def manage_get_uuid( relationship_uuid: str, request_url: str, start_time: datetime.datetime ):
    """ Manages referent-match get for specific uuid.
        Returns context.
        Called by tests, and views.data_referent_match() """
    log.debug( 'starting' )
    try:
        context = {}
        ## get entry ----------------------------------------------------
        session_instance = make_session()        
        match = session_instance.query( models_alch.ReferentMatch ).get( relationship_uuid )
        assert type(match) == models_alch.ReferentMatch or isinstance(match, type(None))
        ## prepare response ---------------------------------------------
        if match:
            response_dct: dict = prepare_common_response_dct( match, start_time )        
            context = {
                'request': {
                    'url': request_url,
                    'method': 'GET',
                    'timestamp': str( start_time )
                },
                'response': response_dct
            }
        else:
            context = { '404': 'Not Found' }
    except Exception as e:
        log.error( f'e, ``{repr(e)}``')
        msg = 'problem with get, or with response-prep; see logs'
        log.exception( msg )
        context = { '500': msg }
    log.debug( f'context, ``{context}``' )
    return context


## UPDATE -----------------------------------------------------------


def manage_put( relationship_uuid: str, request_body, request_url: str, start_time: datetime.datetime ):
    """ Manages referent-match updating -- currently only notes.
        Returns context.
        Called by tests, and views.data_referent_match() """
    log.debug( 'starting' )
    ## validate notes payload ---------------------------------------
    context = {}
    put_payload_dct = {}
    try:
        put_payload_dct: dict = json.loads( request_body )
    except Exception as e:
        msg = 'Bad Request; problem accessing updated researcher-notes'
        log.exception( msg )
        context = { '400': msg }
    ## notes payload is good, so proceed ----------------------------
    try:
        if context == {}:
            ## get entry --------------------------------------------
            session_instance = make_session()        
            match = session_instance.query( models_alch.ReferentMatch ).get( relationship_uuid )
            assert type(match) == models_alch.ReferentMatch or isinstance(match, type(None))
            ## update notes -----------------------------------------
            if match:
                match.date_edited = datetime.datetime.now()
                match.researcher_notes = put_payload_dct['researcher_notes']
                session_instance.add( match )
                session_instance.commit()  # returns None, so no way to verify success
            else:
                context = { '404': 'Not Found' }
            ## prepare response -------------------------------------
            if context == {}:
                match_after_put = session_instance.query( models_alch.ReferentMatch ).get( relationship_uuid )
                assert type(match_after_put) == models_alch.ReferentMatch or isinstance(match_after_put, type(None))
                if match_after_put:
                    response_dct: dict = prepare_common_response_dct( match_after_put, start_time )        
                    context = {
                        'request': {
                            'url': request_url,
                            'method': 'PUT',
                            'payload': put_payload_dct,
                            'timestamp': str( start_time )
                        },
                        'response': response_dct
                    }
                else:
                    context = { '500': 'Server Error; PUT unsuccessful' }
    except Exception as e:
        log.error( f'e, ``{repr(e)}``')
        msg = 'problem with put, or with response-prep; see logs'
        log.exception( msg )
        context = { '500': msg }
    log.debug( f'context, ``{context}``' )
    return context
    ## end def manage_put()


## DELETE -----------------------------------------------------------


def manage_delete( incoming_identifier: str, request_url: str, start_time: datetime.datetime ) -> dict:
    """ Manages referent-match deletion.
        Returns context.
        Called by tests, and views.data_referent_match() """
    log.debug( 'starting manage_delete()' )
    log.debug( f'incoming_identifier, ``{incoming_identifier}``' )
    context = {}
    try:
        session_instance = make_session()
        match_result = session_instance.query( models_alch.ReferentMatch ).filter( 
            models_alch.ReferentMatch.uuid == incoming_identifier ).first()
        assert type(match_result) == models_alch.ReferentMatch or isinstance(match_result, type(None))
        if match_result:
            session_instance.delete( match_result )
            session_instance.commit()
            context = { '200': 'OK' }
        else:
            context = { '404': 'Not Found' }
    except:
        msg = 'problem with delete, or with response-prep; see logs'
        log.exception( msg )
        context = { '500': msg }
    log.debug( f'context, ``{context}``' )
    return context


## HELPERS ==========================================================


def make_session() -> orm.session.Session:
    """ Called by all CRUD types. """
    engine = sqlalchemy.create_engine( settings_app.DB_URL, echo=True )
    Session = orm.sessionmaker( bind=engine )
    session_instance = Session()
    return session_instance


def prepare_common_response_dct( mtch: models_alch.ReferentMatch, start_time: datetime.datetime ) -> dict:
    """ Builds the response-dict.
        Called by manage_post() and probably manage_get_uuid() """
    # assert type(mtch) == models_alch.ReferentMatch
    response_dct = {
        'referent_match_data': {
            'uuid': mtch.uuid,
            'referent_sbj_uuid': mtch.referent_sbj_uuid,
            'referent_obj_uuid': mtch.referent_obj_uuid,
            'date_created': str( mtch.date_created ),
            'date_edited': str( mtch.date_edited ),
            'researcher_notes': mtch.researcher_notes,
            'confidence': mtch.confidence,
        },
        'elapsed_time': str( datetime.datetime.now() - start_time )
    }
    log.debug( f'response_dct, ``{pprint.pformat(response_dct)}``' )
    return response_dct



        # match_result = session_instance.query( models_alch.ReferentMatch ).filter( 
        #     or_(
        #         models_alch.ReferentMatch.referent_sbj_uuid == incoming_identifier, 
        #         models_alch.ReferentMatch.referent_obj_uuid == incoming_identifier
        #     ) 
        # ).all()

