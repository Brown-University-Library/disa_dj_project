# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView
from disa_app import views


admin.autodiscover()


urlpatterns = [

    ## primary app urls...

    url( r'^login/$', views.temp_response, name='login_url' ),
    url( r'^logout/$', views.temp_response, name='temp_name_url' ),

    url( r'^editor/documents/(?P<citeId>.*)/$', views.temp_response, name='temp_name_url' ),
    url( r'^editor/records/(?P<recId>.*)/$', views.temp_response, name='temp_name_url' ),
    url( r'^editor/person/(?P<entId>.*)/$', views.temp_response, name='temp_name_url' ),
    url( r'^editor/$', views.temp_response, name='temp_name_url' ),

    url( r'^data/documents/(?P<docId>.*)/$', views.temp_response, name='temp_name_url' ),  # note, 'citeID' is passed on a PUT.
    url( r'^data/records/(?P<recId>.*)/$', views.temp_response, name='temp_name_url' ),  # note, 'refID' is passed on a PUT.
    url( r'^data/entrants/details/(?P<rntId>.*)/$', views.temp_response, name='temp_name_url' ),
    url( r'^data/entrants/(?P<rntId>.*)/$', views.temp_response, name='temp_name_url' ),
    url( r'^data/reference/(?P<refId>.*)/$', views.temp_response, name='temp_name_url' ),
    url( r'^data/sections/(?P<refId>.*)/relationships/$', views.temp_response, name='temp_name_url' ),
    url( r'^data/relationships/(?P<relId>.*)/$', views.temp_response, name='temp_name_url' ),

    url( r'^people/$', views.people, name='people_url' ),
    url( r'^people/(?P<persId>.*)/$', views.temp_response, name='temp_name_url' ),

    url( r'^source/(?P<srcId>.*)/$', views.temp_response, name='temp_name_url' ),

    url( r'^record/relationships/(?P<recId>.*)/$', views.temp_response, name='temp_name_url' ),

    ## old...

    url( r'^browse/$', views.browse, name='browse_url' ),
    # url( r'^person_index/$', views.person_index, name='person_index_url' ),
    # url( r'^login/$', views.login, name='login_url' ),
    # url( r'^editor_index/$', views.editor_index, name='editor_index_url' ),
    # url( r'^logout/$', views.logout, name='logout_url' ),
    url( r'^admin/', admin.site.urls ),

    ## support urls...

    url( r'^denormalized.json$', views.dnrmlzd_jsn_prx_url, name='dnrmlzd_jsn_prx_url_url' ),
    url( r'^version/$', views.version, name='version_url' ),
    url( r'^error_check/$', views.error_check, name='error_check_url' ),

    # url( r'^$', RedirectView.as_view(pattern_name='browse_url') ),
    url( r'^$', views.temp_response, name='temp_name_url' ),

    # url( r'^admin/login/', RedirectView.as_view(pattern_name='login_url') ),
    # url( r'^login/$', views.login, name='login_url' ),

    ]


# ------------------------
# routes from flask app...
# ------------------------

# @app.route('/login', methods=['GET', 'POST'])
# # def login():

# @app.route('/logout')
# # def logout():

# @app.route('/editor', methods=['GET'])
# # @login_required
# # def editor_index():

# @app.route('/editor/documents')
# @app.route('/editor/documents/<citeId>')
# # @login_required
# # def edit_citation(citeId=None):

# @app.route('/editor/records')
# @app.route('/editor/records/<recId>')
# # @login_required
# # def edit_record(recId=None):

# @app.route('/editor/person')
# @app.route('/editor/person/<entId>')
# # @login_required
# # def edit_entrant(entId=None):

# @app.route('/data/documents/', methods=['GET'])
# @app.route('/data/documents/<docId>', methods=['GET'])
# # @login_required
# # def read_document_data(docId=None):

# @app.route('/data/documents/', methods=['POST'])
# # @login_required
# # def create_citation():

# @app.route('/data/documents/', methods=['PUT'])
# @app.route('/data/documents/<citeId>', methods=['PUT'])
# # @login_required
# # def update_citation_data(citeId):

# @app.route('/data/records/', methods=['GET'])
# @app.route('/data/records/<recId>', methods=['GET'])
# # @login_required
# # def read_record_data(recId=None):

# @app.route('/data/entrants/', methods=['GET'])
# @app.route('/data/entrants/<rntId>', methods=['GET'])
# # @login_required
# # def read_referent_data(rntId=None):

# @app.route('/data/records/', methods=['POST'])
# @app.route('/data/records/<refId>', methods=['PUT'])
# # @login_required
# # def update_reference_data(refId=None):

# @app.route('/data/reference/<refId>', methods=['DELETE'])
# # def delete_reference(refId):

# @app.route('/data/entrants/', methods=['POST'])
# @app.route('/data/entrants/<rntId>', methods=['PUT', 'DELETE'])
# # @login_required
# # def update_referent(rntId=None):

# @app.route('/data/entrants/details/', methods=['PUT'])
# @app.route('/data/entrants/details/<rntId>', methods=['PUT'])
# # @login_required
# # def update_referent_details(rntId):

# @app.route('/people/')
# # def person_index():

# @app.route('/people/<persId>')
# # def get_person(persId):

# @app.route('/source/<srcId>')
# # def get_source(srcId):
# #     return redirect(url_for('edit_record', recId=srcId))

# @app.route('/record/relationships/<recId>')
# # @login_required
# # def edit_relationships(recId):

# @app.route('/data/sections/<refId>/relationships/')
# # @login_required
# # def relationships_by_reference(refId):

# @app.route('/data/relationships/', methods=['POST'])
# # @login_required
# # def create_relationship():

# @app.route('/data/relationships/<relId>', methods=['DELETE'])
# # @login_required
# # def delete_relationship(relId):

# @app.route( '/error_check' )
# # def error_check():
