from rdflib import Namespace, Literal, URIRef
from rdflib.graph import Graph, ConjunctiveGraph
from django.conf import settings
from django.http import HttpResponse
from functools import partial

def build_graph(request, path):
    # depth param not part of URI proper
    s = URIRef(request.build_absolute_uri().split('?')[0]) 
    cg = ConjunctiveGraph(store=request.store)
    def traverse(s, depth=0, graph=None):
        if graph is None:
            graph = Graph()
            [ graph.bind(prefix, uri) 
              for prefix, uri in settings.NAMESPACES.items() ]
        graph += cg.triples((s,None,None))
        if depth > 0:
            map(partial(traverse, depth=depth-1, graph=graph), 
                set(graph.objects(subject=s)))
        return graph
    return traverse(s, depth=int(request.GET.get('depth', 0)))

def resource(request, path):
    g = build_graph(request, path)
    content_type = request.META.get('HTTP_ACCEPT', 'text/turtle')
    if content_type == 'application/json':
        content = g.serialize(format='json-ld', 
                              context=settings.JSON_LD_CONTEXT)
    else:
        content_type = 'text/turtle'
        content = g.serialize(format='turtle')
    return HttpResponse(content, content_type=content_type)

def resource_as_json_ld(request, path):
    g = build_graph(request, path)

def resource_as_turtle(request, path):
    g = build_graph(request, path)
