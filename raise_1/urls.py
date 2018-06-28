from django.contrib import admin
from django.conf.urls import url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^raise_2/', include('raise_2.urls')), #include the urls from raise_2/...
    url(r'^$', include('raise_2.urls')),
]

urlpatterns += staticfiles_urlpatterns()