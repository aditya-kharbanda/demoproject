from django.conf.urls import include, url
urlpatterns = [
    url(r'^login/$', 'account.views.login', name="login"),
    url(r'^logout/$', 'account.views.logout', name="logout"),
    url(r'^home/$', 'account.views.home', name="home"),
]
