# -*- coding: utf-8 -*-

import requests
from rdflib import Graph, URIRef, Literal
from django.conf import settings

@given('an existing subject')
def step(context):
    context.context = {
        "prefLabel": "http://www.w3.org/2004/02/skos/core#prefLabel",
        "name": "http://xmlns.com/foaf/0.1/name",
        "place of birth": "http://www.wikidata.org/wiki/Property:P19",
        "country": "http://www.wikidata.org/wiki/Property:P17",
        "ISO 3166-1 alpha-3": "http://www.wikidata.org/wiki/Property:P298" }

    context.subject = context.browser_url('/topicnode/666')

    graph = Graph(settings.Store(identifier=settings.STORE_ID))
    graph.add(
        (URIRef(context.subject),
         URIRef(context.context['prefLabel']),
         URIRef('http://www.wikidata.org/wiki/Q4115712')))
    graph.add(
        (URIRef('http://www.wikidata.org/wiki/Q4115712'), 
         URIRef(context.context['country']),
         URIRef('http://www.wikidata.org/wiki/Q37')))
    graph.add(
        (URIRef('http://www.wikidata.org/wiki/Q37'),
         URIRef(context.context['ISO 3166-1 alpha-3']),
         Literal('LTU')))

@when('a GET request is received for the subject')
def step(context):
    context.request = requests.get(context.subject)
    
@then('the server provides an RDF representation')
def step(context):
    assert context.request.json() == {
        "@id": context.request.url,
        "@context": context.context,
        "prefLabel": "Emma Goldman",
        "name": [ "Emma Goldman", "エマ・ゴールドマン" ],
        "place of birth": {
            "@id": "http://www.wikidata.org/wiki/Q4115712",
            "country": {
                "@id": "http://www.wikidata.org/wiki/Q37",
                "ISO 3166-1 alpha-3": "LTU",
                }
            }
        }

