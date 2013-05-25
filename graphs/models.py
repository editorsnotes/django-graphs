class GraphMixin(object):
    """
    A mixin for objects with affiliated graphs of data.

    Defines a `graph` attribute with a `using` method that can be
    called to return an rdflib Graph of data affiliated with this
    object. By default, this means the graph in the specified triplestore
    with the identifier matching the object's absolute URL.
    """
    def get_graph_from(self, store):
        return Graph(store, identifier=object.get_absolute_url())
