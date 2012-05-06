from django.conf.urls.defaults import *
from misitio.views.viewsUsuario import registrarUsuario
urlpatterns = patterns('',
(r'^Usuario/registrar_usuario/$',registrarUsuario),
)

