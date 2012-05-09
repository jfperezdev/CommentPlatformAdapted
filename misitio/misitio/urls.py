from django.conf.urls.defaults import *
from misitio.views.viewsUsuario import registrarUsuario,iniciarSesion,modificarUsuario
from misitio.views.viewsComentario import registrarComentario,responderComentario,listarComentario

urlpatterns = patterns('',
(r'^Usuario/registrar_usuario/$',registrarUsuario),
(r'^Usuario/iniciar_sesion/$',iniciarSesion),
(r'^Usuario/modificar_usuario/$',modificarUsuario),
(r'^Comentario/comentar/$',registrarComentario),
(r'^Comentario/responder_comentario/$',responderComentario),
(r'^Comentario/listar_comentarios/([^/]+)$',listarComentario),
)
