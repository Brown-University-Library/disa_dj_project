# -*- coding: utf-8 -*-

"""
WSGI config.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

"""
Note: no need to activate the virtual-environment here for passenger.
- the project's httpd/passenger.conf section allows specification of the python-path via `PassengerPython`, which auto-activates it.
- the auto-activation provides access to modules, but not, automatically, env-vars.
- passenger env-vars loading under python3.x is enabled via the `SenEnv` entry in the project's httpd/passenger.conf section.
  - usage: `SetEnv PREFIX__ENV_SETTINGS_PATH /path/to/project_env_settings.sh`
  - `SenEnv` requires apache env_module; info: <https://www.phusionpassenger.com/library/indepth/environment_variables.html>,
     enabled by default on macOS 10.12.4, and our dev and production servers.

For activating the virtual-environment manually, don't source the settings file directly. Instead, add to `project_env/bin/activate`:
  export PREFIX__ENV_SETTINGS_PATH="/path/to/project_env_settings.sh"
  source $PREFIX__ENV_SETTINGS_PATH
This allows not only the sourcing, but also creates the env-var used below by shellvars.
"""

import os, pprint, sys
import shellvars
from django.core.wsgi import get_wsgi_application


# print( 'the initial env, ```{}```'.format( pprint.pformat(dict(os.environ)) ) )

PROJECT_DIR_PATH = os.path.dirname( os.path.dirname(os.path.abspath(__file__)) )
ENV_SETTINGS_FILE = os.environ['DISA_DJ__ENV_SETTINGS_PATH']  # set in `httpd/passenger.conf`, and `env/bin/activate`

## update path
sys.path.append( PROJECT_DIR_PATH )

## reference django settings
os.environ[u'DJANGO_SETTINGS_MODULE'] = 'config.settings'  # so django can access its settings

## load up env vars
var_dct = shellvars.get_vars( ENV_SETTINGS_FILE )
for ( key, val ) in var_dct.items():
    os.environ[key.decode('utf-8')] = val.decode('utf-8')

# print( 'the final env, ```{}```'.format( pprint.pformat(dict(os.environ)) ) )

## gogogo
application = get_wsgi_application()
