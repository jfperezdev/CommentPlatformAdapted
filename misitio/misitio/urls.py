from django.conf.urls.defaults import *
from misitio.views.viewsUsuario import registrarUsuario
from misitio.views.viewsComentario import registrarComentario

urlpatterns = patterns('',
(r'^Usuario/registrar_usuario/$',registrarUsuario),
(r'^Comentario/Comentar/$',registrarComentario),
)

