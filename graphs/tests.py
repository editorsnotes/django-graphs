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

def create_subject(context):
    context['context'] = settings.JSON_LD_CONTEXT
    context['subject'] = u"http://testserver/topicnode/666"
    
    store = get_store()

    # example scenario, just for illustration. the subgraphs can be
    # used however one wants.
    emma = URIRef(context['subject'])
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
    q = {'depth':context['depth']} if 'depth' in context else {}
    context['client'] = Client()
    context['response'] = context['client'].get(context['subject'], q)

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

def assert_json(context, expect):
    data = json.loads(context['response'].content) 
    context['case'].maxDiff = None
    context['case'].assertMultiLineEqual(
        canonical_json(expect), canonical_json(data))

def check_json_ld_depth_0(context):
    assert_json(context, {
            u"@context": context['context'],
            u"@id": context['subject'],
            u"prefLabel": u"Emma Goldman",
            u"place of birth": {
                u"@id": u"http://www.wikidata.org/wiki/Q4115712" },
            u"name": [ 
                { u"@value": u"Emma Goldman", u"@language": u"en" },
                { u"@value": u"エマ・ゴールドマン", u"@language": u"ja" }] })

def check_json_ld_depth_2(context):
    # multiple subjects results in different JSON-LD layout
    assert_json(context, {
            u"@context": context['context'],
            u"@graph": [
                { u"@id": context['subject'],
                  u"name": [
                        { u"@value": u"Emma Goldman", u"@language": u"en" },
                        { u"@value": u"エマ・ゴールドマン", u"@language": u"ja" },
                        ],
                  u"place of birth": {
                        u"@id": u"http://www.wikidata.org/wiki/Q4115712"},
                  u"prefLabel": u"Emma Goldman" },
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
        
    def test_get_existing_subject(self, context={}):
        self.feature_test(
        (create_subject,),
        (make_get_request,),
        (check_json_ld,))

    def test_get_existing_subject_depth_2(self):
        def depth_2(c): c['depth']=2
        self.feature_test(
        (create_subject, var('depth', 2)),
        (make_get_request,),
        (check_json_ld,))

    def tearDown(self):
        get_store().destroy(Literal(settings.STORE['CONFIG']))
