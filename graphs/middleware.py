from rdflib import plugin, URIRef, Literal
from rdflib.store import Store
from django.conf import settings

class SQLAlchemyStore(object):
    def process_request(self, request):
        request.store = plugin.get(settings.STORE['TYPE'], Store)(
            URIRef(settings.STORE['ID']) 
            if 'ID' in settings.STORE else None,
            Literal(settings.STORE['CONFIG']) 
            if 'CONFIG' in settings.STORE else None)
        return None

    def process_exception(self, request, exception):
        store = getattr(request, 'store', None)
        if store is not None:
            store.rollback()
            store.close()
        return None

    def process_response(self, request, response):
        store = getattr(request, 'store', None)
        if store is not None:
            store.close()
        return response
