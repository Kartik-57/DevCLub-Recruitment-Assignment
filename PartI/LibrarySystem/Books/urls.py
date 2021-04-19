from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'books'

urlpatterns = [
    # /books/
    url('^$', views.IndexView.as_view(), name='index'),

    # /books/id/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
]