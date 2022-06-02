import datetime, json, logging, pprint, uuid

import sqlalchemy
from disa_app import models_sqlalchemy as models_alch
from disa_app import settings_app
from sqlalchemy import orm


log = logging.getLogger(__name__)


def manage_get_meta( request_url: str, start_time: datetime.datetime ):
    return {}


def manage_get_all( request_url: str, start_time: datetime.datetime ):
    return {}


def manage_get_uuid( incoming_identifier: str, request_url: str, start_time: datetime.datetime ):
    return {}


def manage_put( incoming_identifier: str, request_body, request_url: str, start_time: datetime.datetime ):
    return {}


def manage_post( request_body: str, request_url: str, start_time: datetime.datetime ) -> dict:
    log.debug( f'request_body, ``{request_body}``' )
    log.debug( f'request_url, ``{request_url}``' ) 
    ## extract data -----------------------------
    post_data: dict = json.loads( request_body )
    log.debug( f'post_data, ``{pprint.pformat(post_data)}``' )
    rfrnt_sub_uuid: str = post_data['rfrnt_sub_uuid']
    rfrnt_obj_uuid: str = post_data['rfrnt_obj_uuid']
    researcher_notes: str = post_data['researcher_notes']
    confidence: int = post_data['confidence']
    uid: str = uuid.uuid4().hex
    ## create new entry -------------------------
    match = models_alch.ReferentMatch()
    match.uuid = uid
    match.referent_A_uuid = rfrnt_sub_uuid
    match.referent_B_uuid = rfrnt_obj_uuid
    match.confidence = confidence
    match.researcher_notes = researcher_notes
    match.date_created = datetime.datetime.now()
    match.date_edited = datetime.datetime.now()
    ## save it ----------------------------------
    session_instance = make_session()
    session_instance.add( match )
    session_instance.commit()  # returns None, so no way to verify success
    match_data: dict = { 'match_uuid': match.uuid }
    return match_data


def make_session() -> orm.session.Session:
    engine = sqlalchemy.create_engine( settings_app.DB_URL, echo=True )
    Session = orm.sessionmaker( bind=engine )
    session_instance = Session()
    return session_instance


    # def execute_post_save( self, count, count_estimated, description, reference_id, user_id ) -> dict:
    #     """ Updates db and returns data.
    #         Called by manage_post() """
    #     log.debug( 'starting Poster.execute_save()' )
    #     assert ( type(count), type(count_estimated), type(description), type(reference_id), type(user_id) ) == (
    #         int, bool, str, int, int )
    #     grp = models_alch.Group()
    #     uid = uuid.uuid4().hex
    #     assert type(uid) == str
    #     grp.uuid = uid
    #     grp.count = count
    #     grp.count_estimated = count_estimated
    #     grp.description = description
    #     grp.reference_id = reference_id
    #     grp.date_created = datetime.datetime.now()
    #     grp.date_modified = datetime.datetime.now()
    #     self.session.add( grp )
    #     self.session.commit()  # returns None, so no way to verify success
    #     self.common.stamp_edit( user_id, grp.reference, self.session )
    #     log.debug( f'returning uuid, ``{uid}``' )
    #     return grp.uuid



def manage_delete( incoming_identifier: str, request_url: str, start_time: datetime.datetime ):
    return {}