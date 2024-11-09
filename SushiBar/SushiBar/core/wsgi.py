import os
import sys
import site
from django.core.wsgi import get_wsgi_application

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/home/jasiu/Publiczny/PSushiBar/SushiBar/venv/lib/python3.6/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('/home/jasiu/Publiczny/PSushiBar/SushiBar/SushiBar')
sys.path.append('/home/jasiu/Publiczny/PSushiBar/SushiBar/SushiBar/core')

#to set enviroment settings for Django apps
os.environ['DJANGO_SETTINGS_MODULE'] = 'SushiBar.settings'

# Activate your virtual env
activate_env=os.path.expanduser('/home/jasiu/Publiczny/PSushiBar/SushiBar/venv/bin/activate_this.py')
exec(open(activate_env).read(), {'__file__': activate_env})

application = get_wsgi_application()

