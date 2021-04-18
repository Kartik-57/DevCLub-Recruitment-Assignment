from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'books'

urlpatterns = [
    # /books/
    url('^$', views.index, name='index'),

    # /books/id/
    url(r'^(?P<book_id>[0-9]+)/$', views.detail, name='detail'),
]