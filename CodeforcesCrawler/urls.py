from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^difficulty/$', views.difficulties_view, name='diffs'),
    url(r'^tags/$', views.tags_view, name='tags'),
]