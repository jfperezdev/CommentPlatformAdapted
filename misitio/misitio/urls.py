from django.conf.urls.defaults import *
from misitio.views.viewsUsuario import registrarUsuario,iniciarSesion,modificarUsuario,eliminarUsuario
from misitio.views.viewsComentario import registrarComentario,responderComentario,listarComentario,meGusta,eliminarComentarios,listarRespuesta,listarEtiqueta,cuentaMeGusta,cuentaNoMeGusta


urlpatterns = patterns('',
(r'^Usuario/registrar_usuario/$',registrarUsuario),
(r'^Usuario/iniciar_sesion/$',iniciarSesion),
(r'^Usuario/modificar_usuario/$',modificarUsuario),
(r'^Usuario/eliminar_usuario/$',eliminarUsuario),
(r'^Comentario/comentar/$',registrarComentario),
(r'^Comentario/responder_comentario/$',responderComentario),
(r'^Comentario/listar_comentarios/([^/]+)$',listarComentario),
(r'^Comentario/listar_respuestas/$',listarRespuesta),
(r'^Comentario/listar_comentarios_con_etiqueta/([^/]+)$',listarEtiqueta),
(r'^Comentario/me_Gusta/$',meGusta),
(r'^Comentario/me_Gusta/contar_me_gusta/$',cuentaMeGusta),
(r'^Comentario/me_Gusta/contar_no_me_gusta/$',cuentaNoMeGusta),
(r'^Comentario/eliminar_comentario/$',eliminarComentarios),
)
