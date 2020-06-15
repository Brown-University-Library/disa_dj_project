import logging, pprint

from disa_app.models import UserProfile
# from django.contrib.auth import get_backends, login
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect


log = logging.getLogger(__name__)


def run_authentication( request ):
    """ Validates params.
        Returns boolean.
        Called by views.user_pass_handler() """
    log.debug( f'initial request.session.__dict__, ``{pprint.pformat(request.session.__dict__)}``' )
    return_val = False
    log.debug( 'request.POST, `%s`' % pprint.pformat(request.POST) )
    if sorted( request.POST.keys() ) == [ 'csrfmiddlewaretoken', 'manual_login_password', 'manual_login_username' ]:
        log.debug( 'keys good' )
        received_username = request.POST['manual_login_username']
        received_password = request.POST['manual_login_password']
        log.debug( 'about to start try block' )
        try:
            usr = authenticate(request, username=received_username, password=received_password)
            log.debug( f'usr, ``{usr}``' )
            if usr is not None:  # usr found
                log.debug( 'login legit' )
                login( request, usr )
                log.debug( 'user logged in' )
                request.session['manual_login_username'] = None
                request.session['manual_login_password'] = None
                return_val = True
            else:  # usr not found
                request.session['manual_login_username'] = received_username
                request.session['manual_login_password'] = received_password
        except:
            request.session['manual_login_username'] = received_username
            request.session['manual_login_password'] = received_password
            log.exception( f'username, ``{received_username}`` not found; traceback follows, but processing continues' )
    log.debug( f'updated request.session.__dict__, ``{pprint.pformat(request.session.__dict__)}``' )
    log.debug( 'return_val, `%s`' % return_val )
    return return_val


def prep_login_redirect( request ):
    """ Prepares redirect response-object back to views.login() on problems.
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
    redirect_url = reverse( 'editor_index_url' )
    log.debug( 'redirect_url, `%s`' % redirect_url )
    resp = HttpResponseRedirect( redirect_url )
    log.debug( 'returning user_pass_handler response' )
    return resp
