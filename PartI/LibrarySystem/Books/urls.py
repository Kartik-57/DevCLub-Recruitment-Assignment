from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib import admin

app_name = 'books'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup/$', views.SignUp, name='signup'),
    url(r'^login/$', views.Login, name='login'),
    url(r'^logout/$', views.Logout, name='logout'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'books/add/$', views.BookCreate.as_view(), name='book-add'),
    url(r'books/(?P<pk>[0-9]+)/$', views.BookUpdate.as_view(), name='book-update'),
    url(r'books/(?P<pk>[0-9]+)/delete/$', views.BookDelete.as_view(), name='book-delete'),
    url(r'^manage-requests/$', views.Manage_Requests, name='manage-requests'),
    url(r'^accept_request/$', views.accept_request, name='accept_request'),
    url(r'^reject_request/$', views.reject_request, name='reject_request'),
    url(r'^make_request/$', views.make_request, name='make_request'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^cancel_request/$', views.cancel_request, name='cancel_request'),
    url(r'^extend_request/$', views.extend_request, name='extend_request'),
    url(r'^accept_ext/$', views.accept_ext, name='accept_ext'),
    url(r'^reject_ext/$', views.reject_ext, name='reject_ext'),
    url(r'^return_book/$', views.return_book, name='return_book'),
    url(r'^review/add/$', views.ReviewCreate.as_view(), name='review-add'),
    path('admin/', admin.site.urls, name='admin'),
]