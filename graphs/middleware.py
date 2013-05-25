from rdflib.store import Store

class SQLAlchemyStore(object):
    def process_request(self, request):
        request.store = settings.Store(
            identifier=settings.store_id, 
            configuration=settings.store_config)

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
