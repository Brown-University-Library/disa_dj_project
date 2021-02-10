# -*- coding: utf-8 -*-

import logging, pprint

# import sqlalchemy
# from disa_app import models_sqlalchemy as models_alch
# from disa_app import settings_app
# from disa_app.lib import person_common
# from django.conf import settings
# from django.core.urlresolvers import reverse
# from django.http import HttpResponse
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker


log = logging.getLogger(__name__)


def check_browse_logged_in( session_items, is_logged_in_via_django ):
    log.debug( f'session_items start, ``{pprint.pformat(session_items)}``' )
    log.debug( f'type(session_items), ``{type(session_items)}``' )
    log.debug( f'is_logged_in_via_django start, ``{is_logged_in_via_django}``' )
    log.debug( f'type(is_logged_in_via_django), ``{type(is_logged_in_via_django)}``' )
    # assert type( session_items ) == type( {}.items() )
    assert type( session_items ) == dict
    assert type( is_logged_in_via_django ) == bool
    is_logged_in = False
    if is_logged_in_via_django:
        is_logged_in = True
    elif session_items.get( 'browse_logged_in', "no" ) == "yes":
        is_logged_in = True
    return is_logged_in
