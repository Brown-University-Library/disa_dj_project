# -*- coding: utf-8 -*-

import datetime, json, logging, os, pprint
from typing import List

import requests
from disa_app import settings_app
from disa_app.lib import view_data_entrant_manager  # api/people
from disa_app.lib import view_data_records_manager  # api/items
from disa_app.lib import view_edit_record_manager
from disa_app.lib import view_editor_index_manager, view_edit_citation_manager  # documents
from disa_app.lib import view_info_manager
from disa_app.lib import view_people_manager, view_person_manager, view_edit_referent_manager  # people
from disa_app.lib import view_read_document_data_manager
from disa_app.lib import view_search_results_manager
from disa_app.lib.shib_auth import shib_login  # decorator
from django.conf import settings as project_settings
from django.contrib.auth import logout as django_logout
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render


log = logging.getLogger(__name__)


# ===========================
# main urls
# ===========================


def temp_response( request ):
    requested_path = request.META.get( 'PATH_INFO', 'path_unknown' )
    log.debug( f'requested_path, ```{requested_path}```' )
    return HttpResponse( f'`{requested_path}` handling coming' )


def browse( request ):
    """ Displays home page. """
    log.debug( '\n\nstarting browse()' )
    context = {
        'denormalized_json_url': reverse('dnrmlzd_jsn_prx_url_url'),
        'info_image_url': f'{project_settings.STATIC_URL}images/info.png',
        'logout_next': reverse( 'browse_url' ) }
    if request.user.is_authenticated:
        context['user_is_authenticated'] = True
        context['user_first_name'] = request.user.first_name
    if request.GET.get('format', '') == 'json':
        resp = HttpResponse( json.dumps(context, sort_keys=True, indent=2), content_type='application/json; charset=utf-8' )
    else:
        resp = render( request, 'disa_app_templates/browse.html', context )
    return resp


def people( request ):
    log.debug( '\n\nstarting people()' )
    people: List(dict) = view_people_manager.query_people()
    context = { 'people': people }
    if request.user.is_authenticated:
        context['user_is_authenticated'] = True
        context['user_first_name'] = request.user.first_name
    if request.GET.get('format', '') == 'json':
        resp = HttpResponse( json.dumps(context, sort_keys=True, indent=2), content_type='application/json; charset=utf-8' )
    else:
        resp = render( request, 'disa_app_templates/people.html', context )
    return resp


def person( request, prsn_id ):
    log.debug( f'\n\nstarting person(), with prsn_id, `{prsn_id}`' )
    context: dict = view_person_manager.query_person( prsn_id )
    if request.user.is_authenticated:
        context['user_is_authenticated'] = True
        context['user_first_name'] = request.user.first_name
    if request.GET.get('format', '') == 'json':
        resp = HttpResponse( json.dumps(context, sort_keys=True, indent=2), content_type='application/json; charset=utf-8' )
    else:
        resp = render( request, 'disa_app_templates/person_view.html', context )
    return resp


def source( request, src_id ):
    log.debug( f'\n\nstarting source(), with src_id, `{src_id}`' )
    redirect_url = reverse( 'edit_record_url', kwargs={'rec_id': src_id} )
    log.debug( f'redirect_url, ```{redirect_url}```' )
    return HttpResponseRedirect( redirect_url )


@shib_login
def editor_index( request ):
    ## TODO: rename this url from `/editor/` to `/documents/`?
    log.debug( '\n\nstarting editor_index()' )
    context: dict = view_editor_index_manager.query_documents( request.user.username, request.user.profile.old_db_id )
    if request.user.is_authenticated:
        context['user_is_authenticated'] = True
        context['user_first_name'] = request.user.first_name
    if request.GET.get('format', '') == 'json':
        resp = HttpResponse( json.dumps(context, sort_keys=True, indent=2), content_type='application/json; charset=utf-8' )
    else:
        resp = render( request, 'disa_app_templates/document_index.html', context )
    return resp


def search_results( request ):
    log.debug( '\n\nstarting search_results()' )
    srch_txt = request.GET.get( 'query', None )
    log.debug( f'query, ```{srch_txt}```'  )
    if srch_txt is None:
        redirect_url = request.META.get( 'HTTP_REFERER', reverse('people_url') )
        log.debug( f'empty search, redirecting back to, ```{redirect_url}```' )
        return HttpResponseRedirect( redirect_url )
    context: dict = view_search_results_manager.run_search( srch_txt[0:50] )
    # return HttpResponse( 'search_results coming' )

    if request.user.is_authenticated:
        context['user_is_authenticated'] = True
        context['user_first_name'] = request.user.first_name
    if request.GET.get('format', '') == 'json':
        resp = HttpResponse( json.dumps(context, sort_keys=True, indent=2), content_type='application/json; charset=utf-8' )
    else:
        resp = render( request, 'disa_app_templates/search_results.html', context )
    return resp


# ===========================
# auth urls
# ===========================


@shib_login
def login( request ):
    """ Handles authNZ, & redirects to admin.
        Called by click on login or admin link. """
    log.debug( '\n\nstarting login()' )
    next_url = request.GET.get( 'next', None )
    log.debug( f'next_url, ```{next_url}```' )
    if not next_url:
        log.debug( f'session_keys, ```{list( request.session.keys() )}```' )
        if request.session.get( 'redirect_url', None ):
            redirect_url = request.session['redirect_url']
        else:
            redirect_url = reverse( 'editor_index_url' )
    else:
        redirect_url = request.GET['next']  # may be same page
    if request.session.get( 'redirect_url', None ):  # cleanup
        del request.session['redirect_url']
    log.debug( 'redirect_url, ```%s```' % redirect_url )
    return HttpResponseRedirect( redirect_url )


def logout( request ):
    """ Logs _app_ out; shib logout not yet implemented.
        Called by click on Welcome/Logout link in header-bar. """
    redirect_url = request.GET.get( 'next', None )
    if not redirect_url:
        redirect_url = reverse( 'info_url' )
    django_logout( request )
    log.debug( 'redirect_url, ```%s```' % redirect_url )
    return HttpResponseRedirect( redirect_url )


# ===========================
# editor urls
# ===========================


@shib_login
def edit_citation( request, cite_id ):
    ## url( r'^editor/documents/(?P<cite_id>.*)/$' -- 'edit_citation_url'
    ## TODO: rename function to `edit_document()`?
    # return HttpResponse( 'coming' )
    log.debug( '\n\nstarting edit_citation()' )
    context: dict = view_edit_citation_manager.query_data( cite_id )
    if request.user.is_authenticated:
        context['user_is_authenticated'] = True
        context['user_first_name'] = request.user.first_name
    if request.GET.get('format', '') == 'json':
        resp = HttpResponse( json.dumps(context, sort_keys=True, indent=2), content_type='application/json; charset=utf-8' )
    else:
        resp = render( request, 'disa_app_templates/document_edit.html', context )
    return resp


@shib_login
def edit_person( request, rfrnt_id=None ):
    """ Url: '/editor/person/<rfrnt_id>/' -- 'edit_person_url' """
    log.debug( '\n\nstarting edit_person()' )
    context: dict = view_edit_referent_manager.prep_context( rfrnt_id, request.user.first_name, bool(request.user.is_authenticated) )
    if request.GET.get('format', '') == 'json':
        resp = HttpResponse( json.dumps(context, sort_keys=True, indent=2), content_type='application/json; charset=utf-8' )
    else:
        resp = render( request, 'disa_app_templates/entrant_edit.html', context )
    return resp


@shib_login
def edit_record( request, rec_id ):
    """ Url: '/editor/records/<rec_id>/' -- 'edit_record_url' """
    log.debug( f'\n\nstarting edit_record(), with rec_id, `{rec_id}`' )
    context: dict = view_edit_record_manager.prep_context( rec_id, request.user.first_name, bool(request.user.is_authenticated) )
    if request.GET.get('format', '') == 'json':
        resp = HttpResponse( json.dumps(context, sort_keys=True, indent=2), content_type='application/json; charset=utf-8' )
    else:
        resp = render( request, 'disa_app_templates/record_edit.html', context )
    return resp


@shib_login
def edit_relationships( request, rec_id: str ):
    """ Note: though this is in the 'editor' section here, the url is `/record/relationships/`. """
    return HttpResponse( 'edit-relationships coming' )


@shib_login
def new_citation( request ):
    return HttpResponse( 'new-citation (new-document) coming' )


# ===========================
# data urls
# ===========================


@shib_login
def data_entrants( request, rfrnt_id: str ):
    """ Called via ajax by views.edit_record()
        Url: '/data/entrants/<rfrnt_id>/' -- 'data_referent_url' """
    if request.method == 'GET':
        log.debug( 'get detected' )
        data_entrant_getter = view_data_entrant_manager.Getter()
        resp = data_entrant_getter.manage_get( rfrnt_id )
    elif request.method == 'PUT':
        log.debug( 'put detected' )
        data_entrant_updater = view_data_entrant_manager.Updater()
        resp = data_entrant_updater.manage_put( request.body, request.user.id, rfrnt_id )
    elif request.method == 'POST':
        msg = 'data_entrants() post-handling coming'
        log.debug( msg )
        resp = HttpResponse( msg )
    else:
        msg = 'data_entrants() other request.method handling coming'
        log.warning( f'message returned, ```{msg}``` -- but we shouldn\'t get here' )
        resp = HttpResponse( msg )
    return resp


@shib_login
def data_entrants_details( request, rfrnt_id ):
    """ Called via ajax by views.edit_person()
        Url: 'data/entrants/details/<rfrnt_id>' -- 'data_entrants_details_url' """
    return HttpResponse( 'data_entrants_details_url response coming' )


@shib_login
def data_records( request, rec_id ):
    """ Called via ajax by views.edit_record()
        Url: '/data/records/<rec_id>/' -- 'data_record_url' """
    log.debug( f'\n\nstarting data_records person(), with rec_id, `{rec_id}`' )
    context: dict = view_data_records_manager.query_record( rec_id )
    resp = HttpResponse( json.dumps(context, sort_keys=True, indent=2), content_type='application/json; charset=utf-8' )
    return resp


@shib_login
def read_document_data( request, docId ):
    """ Called via ajax by views.edit_citation()
        Url: '/data/documents/<docId>/' -- 'data_documents_url' """
    log.debug( f'\n\nstarting read_document_data(), with docId, `{docId}`' )
    context: dict = view_read_document_data_manager.query_document( docId, request.user.profile.old_db_id )
    resp = HttpResponse( json.dumps(context, sort_keys=True, indent=2), content_type='application/json; charset=utf-8' )
    return resp


# ===========================
# helper urls
# ===========================


def dnrmlzd_jsn_prx_url( request ):
    """ Allows ajax loading of json from browse() view. """
    r = requests.get( settings_app.DENORMALIZED_JSON_URL )
    return HttpResponse( r.content, content_type='application/json; charset=utf-8' )


# ===========================
# for development convenience
# ===========================


def version( request ):
    """ Returns basic data including branch & commit. """
    # log.debug( 'request.__dict__, ```%s```' % pprint.pformat(request.__dict__) )
    rq_now = datetime.datetime.now()
    commit = view_info_manager.get_commit()
    branch = view_info_manager.get_branch()
    info_txt = commit.replace( 'commit', branch )
    resp_now = datetime.datetime.now()
    taken = resp_now - rq_now
    context_dct = view_info_manager.make_context( request, rq_now, info_txt, taken )
    output = json.dumps( context_dct, sort_keys=True, indent=2 )
    return HttpResponse( output, content_type='application/json; charset=utf-8' )


def error_check( request ):
    """ For an easy way to check that admins receive error-emails (in development).
        To view error-emails in runserver-development:
        - run, in another terminal window: `python -m smtpd -n -c DebuggingServer localhost:1026`,
        - (or substitue your own settings for localhost:1026)
    """
    if project_settings.DEBUG == True:
        1/0
    else:
        return HttpResponseNotFound( '<div>404 / Not Found</div>' )






# # ==========
# # works
# # ==========
# from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy import create_engine
# engine = create_engine( settings_app.DB_URL, echo=True )
# from sqlalchemy.ext.declarative import declarative_base
# Base = declarative_base()

# class Citation(Base):
#     __tablename__ = '3_citations'
#     id = Column( Integer, primary_key=True )
#     citation_type_id = Column( Integer, ForeignKey('2_citation_types.id'), nullable=False )
#     display = Column( String(500) )
#     zotero_id = Column( String(255) )
#     # comments = Column( UnicodeText() )
#     acknowledgements = Column( String(255) )
#     # references = db.relationship('Reference', backref='citation', lazy=True)

#     def __repr__(self):
#         return f'<Citation {self.id}>'

# from sqlalchemy.orm import sessionmaker
# Session = sessionmaker(bind = engine)
# session = Session()
# resultset: list = session.query( Citation ).all()
# log.debug( f'type(resultset), `{type(resultset)}`' )

# for row in resultset:
#     citation: sqlalchemy.orm.state.InstanceState = row
#     # log.debug( f'type(row), `{type(row)}`' )
#     # log.debug( f'id, `{row.id}`; display, ```{row.display}```; citation_type_id, `{row.citation_type_id}`' )
#     log.debug( f'citation, ```{pprint.pformat(citation.__dict__)}```' )
#     # break
