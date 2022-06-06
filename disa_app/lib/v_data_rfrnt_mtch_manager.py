import datetime, json, logging, pprint, uuid

import sqlalchemy
from disa_app import models_sqlalchemy as models_alch
from disa_app import settings_app
from sqlalchemy import orm


log = logging.getLogger(__name__)


## CREATE -----------------------------------------------------------

def manage_post( request_body: str, request_url: str, start_time: datetime.datetime ) -> dict:
    log.debug( f'request_body, ``{request_body}``' )
    log.debug( f'request_url, ``{request_url}``' ) 
    ## extract data from post payload -----------
    post_data: dict = json.loads( request_body )
    log.debug( f'post_data, ``{pprint.pformat(post_data)}``' )
    rfrnt_sbj_uuid: str = post_data['rfrnt_sbj_uuid']
    rfrnt_obj_uuid: str = post_data['rfrnt_obj_uuid']
    researcher_notes: str = post_data['researcher_notes']
    confidence: int = post_data['confidence']
    uid: str = uuid.uuid4().hex
    ## create new entry -------------------------
    match = models_alch.ReferentMatch()
    match.uuid = uid
    match.referent_sbj_uuid = rfrnt_sbj_uuid
    match.referent_obj_uuid = rfrnt_obj_uuid
    match.confidence = confidence
    match.researcher_notes = researcher_notes
    match.date_created = datetime.datetime.now()
    match.date_edited = datetime.datetime.now()
    ## save it ----------------------------------
    session_instance = make_session()
    session_instance.add( match )
    session_instance.commit()  # returns None, so no way to verify success
    ## prepare response -------------------------
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
    return context


## READ -------------------------------------------------------------


def manage_get_meta( request_url: str, start_time: datetime.datetime ):
    return {}


def manage_get_all( request_url: str, start_time: datetime.datetime ):
    return {}


def manage_get_uuid( incoming_identifier: str, request_url: str, start_time: datetime.datetime ):
    return {}


## UPDATE -----------------------------------------------------------


def manage_put( incoming_identifier: str, request_body, request_url: str, start_time: datetime.datetime ):
    return {}


## DELETE -----------------------------------------------------------


def manage_delete( incoming_identifier: str, request_url: str, start_time: datetime.datetime ):
    ## try search on sbj-uuid

    ## if fails, try search on obj-uuid

    ## if fails, return 404
    return {}


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
