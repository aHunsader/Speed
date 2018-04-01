from . import views
from django.conf.urls import url

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^signup/$', views.signup, name='signup'),
	url(r'^logout/$', views.logout_view, name='logout'),
	url(r'^login/$', views.login_view, name='login'),
	url(r'^children/$', views.children_view, name='children'),
	url(r'^contact/$', views.contact, name='contact'),
	url(r'^aboutus/$', views.aboutus, name='about')
]