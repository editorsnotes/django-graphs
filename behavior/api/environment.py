import wsgi_intercept
import urlparse
from django.conf import settings
from django.core.handlers.wsgi import WSGIHandler
from rdflib.plugins.memory import IOMemory
from requests.packages import urllib3
from requests.packages.urllib3.connectionpool import (
    HTTPConnection as OriginalHTTPConnection, 
    HTTPSConnection as OriginalHTTPSConnection)
 
def install_opener():
    urllib3.connectionpool.HTTPConnection = wsgi_intercept.WSGI_HTTPConnection
    urllib3.connectionpool.HTTPSConnection = wsgi_intercept.WSGI_HTTPSConnection
    wsgi_intercept.wsgi_fake_socket.settimeout = lambda self, timeout: None

def uninstall_opener():
    urllib3.connectionpool.HTTPConnection = OriginalHTTPConnection
    urllib3.connectionpool.HTTPSConnection = OriginalHTTPSConnection

def before_all(context):
    settings.configure(
        ROOT_URLCONF='graphs.urls',
        DATABASES={'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:' }},
        INSTALLED_APPS=('graphs',),
        MIDDLEWARE_CLASSES=('graphs.middleware.SQLAlchemyStore',),
        STORE_ID='test-store',
        Store=IOMemory,
        TEST_RUNNER='django.test.simple.DjangoTestSuiteRunner',
        TEMPLATE_DEBUG=True)

    from django.test.utils import get_runner
    context.runner = get_runner(settings)(interactive=False)

    install_opener()
    host = context.host = 'localhost'
    port = context.port = 80
    wsgi_intercept.add_wsgi_intercept(host, port, WSGIHandler)

    def browser_url(url):
        return urlparse.urljoin('http://{}:{}/'.format(host,port), url)
    context.browser_url = browser_url

def before_scenario(context, scenario):
    context.runner.setup_test_environment()

def after_scenario(context, scenario):
    context.runner.teardown_test_environment()

def after_all(context):
    uninstall_opener()
    
    
