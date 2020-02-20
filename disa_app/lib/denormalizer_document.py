# -*- coding: utf-8 -*-

import collections, datetime, json, logging, os, pprint, uuid
import sqlalchemy

from disa_app import models_sqlalchemy as models_alch
from disa_app import settings_app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


log = logging.getLogger(__name__)


def make_session() -> sqlalchemy.orm.session.Session:
    engine = create_engine( settings_app.DB_URL, echo=True )
    Session = sessionmaker( bind=engine )
    session = Session()
    return session


def denormalize():
    """ Produces denormalized document-based json representing all data entered.
        Called manually for now. """
    log.debug( 'starting json_for_browse()' )
    start_time = datetime.datetime.now()

    session = make_session()

    output = []

    cites = session.query( models_alch.Citation ).all()

    for ( i, cite ) in enumerate( cites):

        # log.debug( f'len( cite.uuid ), ```{len( cite.uuid )}```' )
        # if cite.uuid == None:
        #     log.debug( 'adding uuid' )
        #     cite.uuid = uuid.uuid4().hex
        #     session.add( cite )
        #     session.commit()
        # else:
        #     log.debug( 'found existing uuid' )

        rfrncs = []
        for rfrnc in cite.references:
            # temp_rfrnc_dct: dict = rfrnc.dictify()

            # rfrnc_roles = []
            # for role in rfrnc.reference_type.roles:
            #     role_dct = {
            #         'role_id_TEMP': role.id,
            #         'role_name': role.name,
            #         'role_name_as_relationship': role.name_as_relationship
            #         }
            #     rfrnc_roles.append( role_dct )

            # rfrnc_roles = []
            # for role in rfrnc.reference_type.roles:

            #     rfrnc_role_rfrnts = []
            #     for rfrnt in role.referents:
            #         rfrnt_dct = {
            #             'referent_id': rfrnt.id,
            #             'referent_age': rfrnt.age,
            #             'referent_sex': rfrnt.sex,
            #             # 'referent_display_name': rfrnt.display_name
            #             }
            #         rfrnc_role_rfrnts.append( rfrnt_dct )

            #     role_dct = {
            #         'role_id_TEMP': role.id,
            #         'role_name': role.name,
            #         'role_name_as_relationship': role.name_as_relationship,
            #         'role_referents': rfrnc_role_rfrnts
            #         }
            #     rfrnc_roles.append( role_dct )

            rfrnts = []
            for rfrnt in rfrnc.referents:

                rfrnt_roles = []
                for role in rfrnt.roles:
                    role_dct = {
                        'role_name': role.name,
                        'name_as_relationship': role.name_as_relationship
                        }
                    rfrnt_roles.append( role_dct )

                rfrnt_dct = {
                    'referent_id': rfrnt.id,
                    'referent_display_name': rfrnt.display_name(),
                    'referent_age': rfrnt.age,
                    'referent_sex': rfrnt.sex,
                    'referent_roles': rfrnt_roles
                    }
                rfrnts.append( rfrnt_dct )

            rfrnc_dct = {
                'reference_id': rfrnc.id,
                'reference_transcription': rfrnc.transcription,

                # 'reference_type_id_TEMP': rfrnc.reference_type_id,
                'reference_type_name': rfrnc.reference_type.name,
                # 'reference_type_roles': rfrnc_roles,

                'reference_referents': rfrnts
                }
            rfrncs.append( rfrnc_dct )


        cite_dct = {
            'citation_id': cite.id,
            # 'citation_uuid': cite.uuid,

            'citation_type_id_TEMP': cite.citation_type_id,
            'citation_type_name': cite.citation_type.name,
            'citation_type_zotero_type_id_TEMP': cite.citation_type.zotero_type_id,
            'citation_type_zotero_type_name': cite.citation_type.zotero_type.name,
            'citation_type_zotero_type_creator_name': cite.citation_type.zotero_type.creator_name,

            'citation_display': cite.display,
            'citation_zotero_id': cite.zotero_id,
            'citation_comments': cite.comments,
            'citation_acknowledgements': cite.acknowledgements,
            'citation_references': rfrncs
            }
        output.append( cite_dct )
        if i > 9:
            break

    log.debug( f'output, ```{pprint.pformat(output)}```' )
    return output
