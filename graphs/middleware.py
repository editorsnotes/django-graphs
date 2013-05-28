from rdflib.store import Store
from django.conf import settings

class SQLAlchemyStore(object):
    def process_request(self, request):
        request.store = settings.Store(
            identifier=getattr(settings, 'STORE_ID', None), 
            configuration=getattr(settings, 'STORE_CONFIG', None))

    def process_exception(self, request, exception):
        store = getattr(request, 'store', None)
        if store is not None:
            store.rollback()
            store.close()

    def process_response(self, request, response):
        store = getattr(request, 'store', None)
        if store is not None:
            sess.close(True)
            return response
