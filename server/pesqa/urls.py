from django.conf.urls import patterns, include, url

from rest_framework.authtoken.views import obtain_auth_token

from api.urls import router

urlpatterns = patterns('',
    url(r'^api/token/', obtain_auth_token, name='api-token'),
    url(r'^api/', include(router.urls)),
)
