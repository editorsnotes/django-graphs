# -*- coding: utf-8 -*-

import sys
import json
from django.conf import settings
from django.test import TestCase
from django.test.client import Client
from rdflib import plugin, Graph, URIRef, Literal
from rdflib.store import Store
from functools import partial

def get_store():
    return plugin.get(settings.STORE['TYPE'], Store)(
        identifier=URIRef(settings.STORE['ID']),
        configuration=Literal(settings.STORE['CONFIG']))

def create_resource(context):
    context['context'] = settings.JSON_LD_CONTEXT
    context['resource'] = u"http://testserver/topicnode/666"
    
    store = get_store()

    # example scenario, just for illustration. the subgraphs can be
    # used however one wants.
    emma = URIRef(context['resource'])
    system = Graph(store, identifier='test_system')
    project = Graph(store, identifier='test_project')
    wikidata = Graph(store, identifier='test_wikidata')

    # preferred labels generated dynamically, cached in system graph
    system.add(
        (emma,
         URIRef(context['context']['prefLabel']),
         Literal('Emma Goldman')))

    # projects may have as many relations as they wish in the graph
    project.add(
        (emma,
         URIRef(context['context']['name']),
         Literal('Emma Goldman', lang='en')))
    project.add(
        (emma,
         URIRef(context['context']['place of birth']),
         URIRef('http://www.wikidata.org/wiki/Q4115712')))

    # (local caches of) external sources can provide some useful extra data
    wikidata.add(
        (emma,
         URIRef(context['context']['name']),
         Literal('エマ・ゴールドマン', lang='ja')))
    wikidata.add(
        (emma,
         URIRef(context['context']['type']),
         URIRef('http://www.wikidata.org/wiki/Q215627')))

    # statements where emma is not the subject may nonetheless be useful
    wikidata.add(
        (URIRef('http://www.wikidata.org/wiki/Q4115712'), 
         URIRef(context['context']['country']),
         URIRef('http://www.wikidata.org/wiki/Q37')))
    wikidata.add(
        (URIRef('http://www.wikidata.org/wiki/Q37'),
         URIRef(context['context']['ISO 3166-1 alpha-3']),
         Literal('LTU')))

def make_get_request(context):
    # 4.2.1 LDPR servers must support the HTTP GET Method for LDPRs.
    accept = context['accept'] if 'accept' in context else None
    q = {'depth':context['depth']} if 'depth' in context else {}
    context['client'] = Client()
    context['response'] = context['client'].get(
        context['resource'], q, HTTP_ACCEPT=accept)

def sort_dict(d):
    def sort_item(i):
        (k,v) = i
        d[k] = sort_value(v)
    map(sort_item, d.items())
    return d
    
def sort_value(v):
    if isinstance(v, dict):
        return sort_dict(v)
    if isinstance(v, list):
        return sorted(v, key=lambda i: canonical_json(i))
    return v

def canonical_json(o):
    return json.dumps(
        sort_value(o), sort_keys=True, indent=2, separators=(',', ': '))

def check_json_ld(context):
    getattr(sys.modules[__name__], 'check_json_ld_depth_{}'.format(
            context['depth'] if 'depth' in context else 0))(context)

def check_turtle(context):
    getattr(sys.modules[__name__], 'check_turtle_depth_{}'.format(
            context['depth'] if 'depth' in context else 0))(context)

def assert_json(context, expect):
    context['case'].assertEqual(
        'application/json', context['response']['Content-Type'])
    data = json.loads(context['response'].content) 
    context['case'].maxDiff = None
    context['case'].assertMultiLineEqual(
        canonical_json(expect), canonical_json(data))

def assert_turtle(context, expect):
    context['case'].assertEqual(
        'text/turtle', context['response']['Content-Type'])
    context['case'].maxDiff = None
    context['case'].assertMultiLineEqual(
        expect.encode('utf-8'), context['response'].content)

def check_turtle_depth_0(context):
    # 4.2.2 LDPR servers must provide a text/turtle representation of
    # the requested LDPR
    assert_turtle(context, u"""@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix wiki: <http://www.wikidata.org/wiki/Property:> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<http://testserver/topicnode/666> a <http://www.wikidata.org/wiki/Q215627> ;
    skos:prefLabel "Emma Goldman" ;
    wiki:P19 <http://www.wikidata.org/wiki/Q4115712> ;
    foaf:name "Emma Goldman"@en,
        "エマ・ゴールドマン"@ja .

""")

def check_turtle_depth_2(context):
    # 4.2.2 LDPR servers must provide a text/turtle representation of
    # the requested LDPR
    assert_turtle(context, u"""@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix wiki: <http://www.wikidata.org/wiki/Property:> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<http://testserver/topicnode/666> a <http://www.wikidata.org/wiki/Q215627> ;
    skos:prefLabel "Emma Goldman" ;
    wiki:P19 <http://www.wikidata.org/wiki/Q4115712> ;
    foaf:name "Emma Goldman"@en,
        "エマ・ゴールドマン"@ja .

<http://www.wikidata.org/wiki/Q37> wiki:P298 "LTU" .

<http://www.wikidata.org/wiki/Q4115712> wiki:P17 <http://www.wikidata.org/wiki/Q37> .

""")

def check_json_ld_depth_0(context):
    # 4.1.2 LDPR servers must provide an RDF representation for LDPRs.
    assert_json(context, {
            u"@context": context['context'],
            u"@id": context['resource'],
            u"prefLabel": u"Emma Goldman",
            u"place of birth": {
                u"@id": u"http://www.wikidata.org/wiki/Q4115712" },
            u"name": [ 
                { u"@value": u"Emma Goldman", u"@language": u"en" },
                { u"@value": u"エマ・ゴールドマン", u"@language": u"ja" }],
            # 4.1.5 LDPRs must use the predicate rdf:type to represent
            # the concept of type.
            # 4.1.6 LDPR representations should have at least one
            # rdf:type set explicitly.
            u"type": {
                u"@id": u"http://www.wikidata.org/wiki/Q215627"}})

def check_json_ld_depth_2(context):
    # 4.1.2 LDPR servers must provide an RDF representation for LDPRs.
    # multiple subjects results in different JSON-LD layout
    assert_json(context, {
            u"@context": context['context'],
            u"@graph": [
                { u"@id": context['resource'],
                  u"name": [
                        { u"@value": u"Emma Goldman", u"@language": u"en" },
                        { u"@value": u"エマ・ゴールドマン", u"@language": u"ja" },
                        ],
                  u"place of birth": {
                        u"@id": u"http://www.wikidata.org/wiki/Q4115712"},
                  u"prefLabel": u"Emma Goldman",
                  # 4.1.5 LDPRs must use the predicate rdf:type to
                  # represent the concept of type.
                  # 4.1.6 LDPR representations should have at least one
                  # rdf:type set explicitly.
                  u"type": {
                        u"@id": u"http://www.wikidata.org/wiki/Q215627"}},
                { u"@id": u"http://www.wikidata.org/wiki/Q37",
                  u"ISO 3166-1 alpha-3": u"LTU" } ,
                { u"@id": u"http://www.wikidata.org/wiki/Q4115712",
                  u"country": {u"@id": u"http://www.wikidata.org/wiki/Q37"} },
                ] })

def setitem(k,v,d): 
    d[k] = v

def var(k,v):
    return partial(setitem,k,v)

class GraphAPITestCase(TestCase):

    def feature_test(self, given, when, then):
        context = {}
        context['case'] = self
        call = lambda f: f(context)
        map(call, given)
        map(call, when)
        map(call, then)
        
    def test_get_existing_resource(self, context={}):
        self.feature_test(
        (create_resource,),
        (make_get_request,),
        (check_turtle,))

    def test_get_existing_resource_depth_2(self, context={}):
        self.feature_test(
        (create_resource, var('depth', 2)),
        (make_get_request,),
        (check_turtle,))

    def test_get_existing_resource_as_json_ld(self, context={}):
        self.feature_test(
        (create_resource, var('accept', 'application/json')),
        (make_get_request,),
        (check_json_ld,))

    def test_get_existing_resource_as_json_ld_depth_2(self):
        self.feature_test(
        (create_resource, var('depth', 2), var('accept', 'application/json')),
        (make_get_request,),
        (check_json_ld,))

    def tearDown(self):
        get_store().destroy(Literal(settings.STORE['CONFIG']))
