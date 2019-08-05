from django.conf.urls import url
from .import views

# SET THE NAMESPACE!
app_name = 'video'

urlpatterns=[
    url(r'^live/$', views.live_video, name='live'),
    url(r'^inicia/$', views.iniciar_video, name='inicia'),
    url(r'^detener/$', views.detener_video, name='detener'),
]