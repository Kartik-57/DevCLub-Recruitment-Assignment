from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'books'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^signup/$', views.UserFormView.as_view(), name='signup'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'books/add/$', views.BookCreate.as_view(), name='book-add'),
    url(r'books/(?P<pk>[0-9]+)/$', views.BookUpdate.as_view(), name='book-update'),
    url(r'books/(?P<pk>[0-9]+)/delete/$', views.BookDelete.as_view(), name='book-delete'),
]