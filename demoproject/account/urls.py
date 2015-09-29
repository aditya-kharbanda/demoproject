from django.conf.urls import include, url
urlpatterns = [
    url(r'^login/$', 'account.views.login', name="login"),
    url(r'^logout/$', 'account.views.logout', name="logout"),
    url(r'^home/$', 'account.views.home', name="home"),
    url(r'^forgot_password/$', 'account.views.forgot_password', name="forgot_password"),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'account.views.reset_password', name='password_reset_confirm'),
]
