

def validate_params( self, request ):
    """ Validates params.
        Returns boolean.
        Called by views.barcode_handler() """
    return_val = False
    log.debug( 'request.POST, `%s`' % pprint.pformat(request.POST) )
    log.debug( "request.POST['pickup_location'], `%s`" % pprint.pformat(request.POST['pickup_location']) )
    if sorted( request.POST.keys() ) == ['barcode_login_barcode', 'barcode_login_name', 'csrfmiddlewaretoken', 'pickup_location']:
        request.session['barcode_login_name'] = request.POST['barcode_login_name']
        request.session['barcode_login_barcode'] = request.POST['barcode_login_barcode']
        request.session['pickup_location'] = request.POST['pickup_location']
        if len(request.POST['barcode_login_name']) > 0 and len(request.POST['barcode_login_barcode']) > 13:
            return_val = True
    log.debug( 'validate_params return_val, `%s`' % return_val )
    return return_val



def prep_login_redirect( self, request ):
    """ Prepares redirect response-object to views.login() on bad source or params or authNZ.
        Called by views.barcode_handler() """
    request.session['barcode_login_error'] = 'Problem with username and password.'
    redirect_url = '%s?bibnum=%s&barcode=%s' % ( reverse('login_url'), request.session['item_bib'], request.session['item_barcode'] )
    log.debug( 'redirect_url, `%s`' % redirect_url )
    resp = HttpResponseRedirect( redirect_url )
    return resp


def authenticate( self, barcode_login_name, barcode_login_barcode ):
    """ Checks submitted login-name and login-barcode; returns boolean.
        Called by views.barcode_handler() """
    return_val = False
    jos_sess = IIIAccount( barcode_login_name, barcode_login_barcode )
    try:
        jos_sess.login()
        return_val = True
        jos_sess.logout()
    except Exception as e:
        log.debug( 'exception on login-try, `%s`' % unicode(repr(e)) )
    log.debug( 'authenticate barcode login check, `%s`' % return_val )
    return return_val

    papi_helper = models.PatronApiHelper()


def authorize( self, patron_barcode ):
    """ Directs call to patron-api service; returns patron name and email address.
        Called by views.barcode_handler() """
    patron_info_dct = False
    papi_helper = PatronApiHelper( patron_barcode )
    if papi_helper.ptype_validity is not False:
        if papi_helper.patron_email is not None:
            patron_info_dct = {
                'patron_name': papi_helper.patron_name,  # last, first middle,
                'patron_email': papi_helper.patron_email }
    log.debug( 'authorize patron_info_dct, `%s`' % patron_info_dct )
    return patron_info_dct

# def authorize( self, patron_barcode ):
#     """ Directs call to patron-api service; returns patron name and email address.
#         Called by views.barcode_handler() """
#     patron_info_dct = False
#     papi_helper = PatronApiHelper( patron_barcode )
#     if papi_helper.ptype_validity is not False:
#         patron_info_dct = {
#             'patron_name': papi_helper.patron_name,  # last, first middle,
#             'patron_email': papi_helper.patron_email }
#     log.debug( 'authorize patron_info_dct, `%s`' % patron_info_dct )
#     return patron_info_dct


def update_session( self, request, patron_info_dct ):
    """ Updates session before redirecting to views.processor()
        Called by views.barcode_handler() """
    request.session['barcode_authorized'] = True
    request.session['josiah_api_name'] = request.session['barcode_login_name']
    request.session['josiah_api_barcode'] = request.session['barcode_login_barcode']
    request.session['user_full_name'] = patron_info_dct['patron_name']
    request.session['user_email'] = patron_info_dct['patron_email']
    return


def prep_processor_redirect( self, request ):
    """ Prepares redirect response-object to views.process() on good login.
        Called by views.barcode_handler() """
    scheme = 'https' if request.is_secure() else 'http'
    redirect_url = '%s://%s%s' % ( scheme, request.get_host(), reverse('processor_url') )
    log.debug( 'redirect_url, `%s`' % redirect_url )
    resp = HttpResponseRedirect( redirect_url )
    log.debug( 'returning barcode_handler response' )
    return resp
