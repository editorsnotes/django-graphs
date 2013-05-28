from django.conf.urls import patterns, url
from graphs import views

urlpatterns = patterns('',
    url(r'^(?P<path>.+)$', views.json_ld, name='json_ld'),
)
