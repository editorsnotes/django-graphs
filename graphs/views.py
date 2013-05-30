from rdflib import Namespace, Literal, URIRef
from rdflib.graph import Graph, ConjunctiveGraph
from django.conf import settings
from django.http import HttpResponse
from functools import partial

def json_ld(request, path):
    # depth param not part of URI proper
    s = URIRef(request.build_absolute_uri().split('?')[0]) 
    cg = ConjunctiveGraph(store=request.store)
    def traverse(s, depth=0, graph=None):
        if graph is None:
            graph = Graph()
        graph += cg.triples((s,None,None))
        if depth > 0:
            map(partial(traverse, depth=depth-1, graph=graph), 
                set(graph.objects(subject=s)))
        return graph
    g = traverse(s, depth=int(request.GET.get('depth', 0)))
    json = g.serialize(format='json-ld', context=settings.JSON_LD_CONTEXT)
    return HttpResponse(json, content_type='application/json')
