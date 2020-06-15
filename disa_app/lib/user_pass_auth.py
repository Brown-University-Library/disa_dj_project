import logging, pprint

from disa_app.models import UserProfile
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect


log = logging.getLogger(__name__)


def validate_params( request ):
    """ Validates params.
        Returns boolean.
        Called by views.user_pass_handler() """
    log.debug( f'initial request.session.__dict__, ``{pprint.pformat(request.session.__dict__)}``' )
    return_val = False
    log.debug( 'request.POST, `%s`' % pprint.pformat(request.POST) )
    if sorted( request.POST.keys() ) == [ 'csrfmiddlewaretoken', 'manual_login_password', 'manual_login_username' ]:
        log.debug( 'keys good' )
        received_username = request.POST['manual_login_username']
        request.session['manual_login_username'] = received_username
        request.session['manual_login_password'] = request.POST['manual_login_password']
        try:
            found_user = UserProfile.objects.get( email=received_username )
            if found_user:
                return_val = True
        except:
            log.exception( f'username, ``{received_username}`` not found; traceback follows, but processing continues' )
    log.debug( f'updated request.session.__dict__, ``{pprint.pformat(request.session.__dict__)}``' )
    log.debug( 'return_val, `%s`' % return_val )
    return return_val


def prep_login_redirect( request ):
    """ Prepares redirect response-object to views.login() on bad source or params or authNZ.
        Called by views.user_pass_handler() """
    request.session['manual_login_error'] = 'Problem with username and password.'
    # redirect_url = '%s?bibnum=%s&barcode=%s' % ( reverse('login_url'), request.session['item_bib'], request.session['item_barcode'] )
    redirect_url = reverse( 'login_url' )
    log.debug( 'redirect_url, `%s`' % redirect_url )
    resp = HttpResponseRedirect( redirect_url )
    return resp


def prep_citations_redirect( request ):
    """ Prepares redirect response-object to citations-list on good login.
        Called by views.user_pass_handler() """
    redirect_url = reverse( 'edit_citation_url' )
    log.debug( 'redirect_url, `%s`' % redirect_url )
    resp = HttpResponseRedirect( redirect_url )
    log.debug( 'returning user_pass_handler response' )
    return resp


# def authenticate( self, barcode_login_name, barcode_login_barcode ):
#     """ Checks submitted login-name and login-barcode; returns boolean.
#         Called by views.barcode_handler() """
#     return_val = False
#     jos_sess = IIIAccount( barcode_login_name, barcode_login_barcode )
#     try:
#         jos_sess.login()
#         return_val = True
#         jos_sess.logout()
#     except Exception as e:
#         log.debug( 'exception on login-try, `%s`' % unicode(repr(e)) )
#     log.debug( 'authenticate barcode login check, `%s`' % return_val )
#     return return_val

#     papi_helper = models.PatronApiHelper()


# def authorize( self, patron_barcode ):
#     """ Directs call to patron-api service; returns patron name and email address.
#         Called by views.barcode_handler() """
#     patron_info_dct = False
#     papi_helper = PatronApiHelper( patron_barcode )
#     if papi_helper.ptype_validity is not False:
#         if papi_helper.patron_email is not None:
#             patron_info_dct = {
#                 'patron_name': papi_helper.patron_name,  # last, first middle,
#                 'patron_email': papi_helper.patron_email }
#     log.debug( 'authorize patron_info_dct, `%s`' % patron_info_dct )
#     return patron_info_dct


# def update_session( self, request, patron_info_dct ):
#     """ Updates session before redirecting to views.processor()
#         Called by views.barcode_handler() """
#     request.session['barcode_authorized'] = True
#     request.session['josiah_api_name'] = request.session['barcode_login_name']
#     request.session['josiah_api_barcode'] = request.session['barcode_login_barcode']
#     request.session['user_full_name'] = patron_info_dct['patron_name']
#     request.session['user_email'] = patron_info_dct['patron_email']
#     return


# def prep_processor_redirect( self, request ):
#     """ Prepares redirect response-object to views.process() on good login.
#         Called by views.barcode_handler() """
#     scheme = 'https' if request.is_secure() else 'http'
#     redirect_url = '%s://%s%s' % ( scheme, request.get_host(), reverse('processor_url') )
#     log.debug( 'redirect_url, `%s`' % redirect_url )
#     resp = HttpResponseRedirect( redirect_url )
#     log.debug( 'returning barcode_handler response' )
#     return resp
