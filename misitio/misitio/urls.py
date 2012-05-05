from django.conf.urls.defaults import *
from misitio.views import usuariosRegistrados,enviarXml,registrarUsuario
urlpatterns = patterns('',
(r'^time/$', usuariosRegistrados),
(r'^time2/$', enviarXml),
(r'^registrarUsuario/$',registrarUsuario),
)

