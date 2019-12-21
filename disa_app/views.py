# -*- coding: utf-8 -*-

import datetime, json, logging, os, pprint
from typing import List

# import sqlalchemy
# from sqlalchemy.orm import sessionmaker as sqla_sessionmaker

import requests
from disa_app import settings_app
from disa_app.lib import view_info_helper
from django.conf import settings as project_settings
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

# from disa_app.lib.shib_auth import shib_login  # decorator


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
    context = {
        'denormalized_json_url': reverse('dnrmlzd_jsn_prx_url_url'),
        'info_image_url': f'{project_settings.STATIC_URL}images/info.png' }
    username = None
    if request.user.is_authenticated:
        username = request.user.first_name
        context['logged_in'] = True
    else:
        context['logged_in'] = False
    context['username'] = username
    if request.GET.get('format', '') == 'json':
        resp = HttpResponse( json.dumps(context, sort_keys=True, indent=2), content_type='application/json; charset=utf-8' )
    else:
        resp = render( request, 'disa_app_templates/browse.html', context )
    return resp


def people( request ):
    log.debug( '\n\nstarting people()' )
    context = {}



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



    from sqlalchemy import Column, Integer, String, ForeignKey
    from sqlalchemy import create_engine
    engine = create_engine( settings_app.DB_URL, echo=True )
    from sqlalchemy.ext.declarative import declarative_base
    Base = declarative_base()

    from sqlalchemy.orm import relationship

    class Person(Base):
        __tablename__ = '1_people'

        id = Column( Integer, primary_key=True )
        first_name = Column( String(255) )
        last_name = Column( String(255) )
        comments = Column( String(255) )
        # references = relationship( 'Referent', backref='person', lazy=True )

        @classmethod
        def filter_on_description( cls, desc ):
            return cls.query.join(
                cls.references).join(Referent.roles).filter(Role.name==desc)

        def display_name( self ):
            display = "{0} {1}".format(
                self.first_name, self.last_name).strip()
            if display == "":
                return "Unknown"
            else:
                return display

        def display_attr( self, attr ):
            vals = { desc.name for ref in self.references
                for desc in getattr(ref, attr) }
            return ', '.join(list(vals))

    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind = engine)
    session = Session()
    # q = Person
    # q = ( Person.id, Person.first_name, Person.last_name, Person.comments )
    # resultset: List(Person) = session.query( q ).all()
    resultset: List(sqlalchemy.util._collections.result) = session.query(
        Person.id, Person.first_name, Person.last_name, Person.comments ).all()

    log.debug( f'type(resultset), `{type(resultset)}`' )

    # <https://stackoverflow.com/questions/19406859/sqlalchemy-convert-select-query-result-to-a-list-of-dicts/20078977>
    # <https://stackoverflow.com/questions/2828248/sqlalchemy-returns-tuple-not-dictionary>

    # for row in resultset:
    #     person: sqlalchemy.util._collections.result = row
    #     log.debug( f'type(row), `{type(row)}`' )
    #     # log.debug( f'person, ```{person.__dict__}```' )
    #     log.debug( f'row, ```{row}```' )
    #     # break

    # j_resultset: List(dict) = [ dict(row) for row in resultset ]

    # j_resultset: List(dict) = [ row.__dict__ for row in resultset ]
    # log.debug( f'j_resultset, ```{pprint.pformat(j_resultset)}```' )

    j_resultset: List(dict) = [ dict( zip(row.keys(), row) ) for row in resultset ]
    log.debug( f'j_resultset, ```{pprint.pformat(j_resultset)}```' )


    # db = SQLAlchemy(app)
    # db_url = settings_app.DB_URL
    # people = []
    # for (prsn, rfrnt) in db.session.query( models.Person, models.Referent ).filter( models.Person.id==models.Referent.id ).all():
    #     sex = rfrnt.sex if rfrnt.sex else "Not Listed"
    #     age = rfrnt.age if rfrnt.age else "Not Listed"
    #     race = None
    #     try:
    #         race = rfrnt.races[0].name
    #     except:
    #         log.debug( 'no race-name; races, ```{rfrnt.races}```' )
    #     race = race if race else "Not Listed"
    #     temp_demographic = f'age, `{age}`; sex, `{sex}`; race, `{race}`'
    #     # prsn.tmp_dmgrphc = temp_demographic
    #     # prsn.last_name = f'{prsn.last_name} ({temp_str})'
    #     prsn.calc_sex = sex
    #     prsn.calc_age = age
    #     prsn.calc_race = race
    #     people.append( prsn )
    # p = people[1]
    # log.debug( f'p.__dict__, ```{p.__dict__}```' )



# class Person(db.Model):
#     __tablename__ = '1_people'

#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(255))
#     last_name = db.Column(db.String(255))
#     comments = db.Column(db.String(255))
#     references = db.relationship('Referent', backref='person', lazy=True)

#     @classmethod
#     def filter_on_description(cls, desc):
#         return cls.query.join(
#             cls.references).join(Referent.roles).filter(Role.name==desc)

#     def display_name(self):
#         display = "{0} {1}".format(
#             self.first_name, self.last_name).strip()
#         if display == "":
#             return "Unknown"
#         else:
#             return display

#     def display_attr(self, attr):
#         vals = { desc.name for ref in self.references
#             for desc in getattr(ref, attr) }
#         return ', '.join(list(vals))


    # context = { 'data': resultset }
    context = { 'data': j_resultset }

    if request.GET.get('format', '') == 'json':
        resp = HttpResponse( json.dumps(context, sort_keys=True, indent=2), content_type='application/json; charset=utf-8' )
    else:
        resp = render( request, 'disa_app_templates/people.html', context )
    return resp


def login( request ):
    return HttpResponse( 'coming' )

def editor_index( request ):
    return HttpResponse( 'coming' )

def logout( request ):
    return HttpResponse( 'coming' )


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
    commit = view_info_helper.get_commit()
    branch = view_info_helper.get_branch()
    info_txt = commit.replace( 'commit', branch )
    resp_now = datetime.datetime.now()
    taken = resp_now - rq_now
    context_dct = view_info_helper.make_context( request, rq_now, info_txt, taken )
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


# @shib_login
# def login( request ):
#     """ Handles authNZ, & redirects to admin.
#         Called by click on login or admin link. """
#     next_url = request.GET.get( 'next', None )
#     if not next_url:
#         redirect_url = reverse( settings_app.POST_LOGIN_ADMIN_REVERSE_URL )
#     else:
#         redirect_url = request.GET['next']  # will often be same page
#     log.debug( 'redirect_url, ```%s```' % redirect_url )
#     return HttpResponseRedirect( redirect_url )
