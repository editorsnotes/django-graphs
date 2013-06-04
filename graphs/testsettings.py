import os
DEBUG = True
DATABASES = {'default': 
             { 'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}}
STORE = {'TYPE':'SQLAlchemy', 
         'ID':'teststore', 
         'CONFIG':'sqlite:///{}/test.sqlite'.format(os.getcwd())}
SECRET_KEY = 'k()96pn_k_b&c3^8+cy!9*$&ievd+rk!amfjskl(c*r!aux-q9'
INSTALLED_APPS = ('graphs',)
ROOT_URLCONF = 'graphs.urls'
MIDDLEWARE_CLASSES = ( 
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'graphs.middleware.SQLAlchemyStore',
    )
NAMESPACES = {
    'foaf': 'http://xmlns.com/foaf/0.1/',
    'skos': 'http://www.w3.org/2004/02/skos/core#',
    'wiki': 'http://www.wikidata.org/wiki/Property:',
    }
JSON_LD_CONTEXT = {
    u"prefLabel": u"http://www.w3.org/2004/02/skos/core#prefLabel",
    u"name": u"http://xmlns.com/foaf/0.1/name",
    u"type": u"http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
    u"place of birth": u"http://www.wikidata.org/wiki/Property:P19",
    u"country": u"http://www.wikidata.org/wiki/Property:P17",
    u"ISO 3166-1 alpha-3": u"http://www.wikidata.org/wiki/Property:P298" }
