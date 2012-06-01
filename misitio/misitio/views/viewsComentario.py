#*********************************************************************************************
#                      Archivo: viewsComentario.py
#                      -------------------
#   copyright            : (C) 2012 by Developer Group: Jose Francisco
#							de Jesus Perez Vera
#                                                       Armen Djenanian Dertorossian
#							Kristian Cortes
# ********************************************************************************************
# PlatformCommentAdapter. Proyecto de Desarrollo del Software
# ********************************************************************************************
# Descripcion : Archivo que contiene la vista Comentario
# ********************************************************************************************

from django.http import HttpResponse
from django.shortcuts import render_to_response
import xml.etree.ElementTree as xml
import misitio.models.Comentario as GestionComentario
import misitio.models.Token as GestionToken
import datetime
import pycassa
from pycassa.pool import ConnectionPool
from pycassa.columnfamily import ColumnFamily
import logging


logger = logging.FileHandler('/home/usuario/ProyectoDesarrolloSoftware/misitio/misitio/logs/logs.log') #inicializacion para el manejo de logs
console = logging.StreamHandler()
logger.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
logger.setFormatter(formatter)
logging.getLogger().addHandler(logger)


############################################################
#----------------- Registrar Comentario--------------------#
#        Rutina creada para registrar un comentario        #
#        el cual contiene la informacion del usuario       #
#        como su nickName, el texto, el token, admite-     #
#	 respuesta y el conjunto de etiquetas que hacen    #
#        referencia al comentario. Este se inserta en      #
#	 persistencia y notifica si ha sido o no satis-	   #
#	 factoria la respuesta.				   #
############################################################
def registrarComentario(request):
    datosComentario =  request.raw_post_data
    tree = xml.fromstring(datosComentario)  
    for i in tree.iter(): 
	if i.tag == "nickName":
	    nickName = i.text
	elif i.tag == "texto":
	    texto = i.text
	elif i.tag == "token":
	    token = i.text
	elif i.tag == "admiteRespuesta":
	    admiteRespuesta = i.text
        elif i.tag == "etiquetas":
	    etiquetas = i.text
    now = datetime.datetime.now()
    elComentario = GestionComentario.Comentario()
    elComentario.nickName = nickName
    elComentario.texto = texto
    elComentario.token = token
    elComentario.admiteRespuesta = admiteRespuesta
    elComentario.fecha = str (now)
    elToken = GestionToken.Token()
    ip = str(request.META['REMOTE_ADDR']) 
    elToken.token = token
    elToken.nickName = nickName
    elToken.ip = ip
  
    miToken = elToken.validarToken()
      
    if  miToken == "TRUE":
	elId = elComentario.registrarComentario(etiquetas)
        if elId != "FALSE":
       	    return render_to_response('nuevoComentario.xml', {'mensajeRespuesta': "Se ha agregado satisfactoriamente el Comentario el dia: "+elComentario.fecha,'idComentario': elId},mimetype='application/xml')
	else:
	    logging.error('EC-012:Conexion no valida para el medio de persistencia al tratar de agregar un comentario')	
       	    return render_to_response('errorMensaje.xml', {'errorMensaje': "Error al tratar de generar el Comentario el dia:" +elComentario.fecha},mimetype='application/xml')
    elif miToken =="Error":
	logging.error('EC-013:Error el usuario '+nickName+ ' tiene un token vigente')
        return render_to_response('errorMensaje.xml', {'errorMensaje': "Lo sentimos el tiempo de su token ha expirado. Vuelva a Iniciar Sesion"},mimetype='application/xml')
    else:
        logging.error('EC-014:Error el usuario '+nickName+ ' envio un token incorrecto')
        return render_to_response('errorMensaje.xml', {'errorMensaje': "Error el token enviado es incorrecto"},mimetype='application/xml')
	
############################################################
#----------------- Responder Comentario--------------------#
#	Procedimiento creado para responder a un           #
#       comentario dado el idComentario y el nickName      #
#       del creador, entonces este envia una respuesta     #
#       en la cual debe poseer un token valido y podra     #
#	registrar en persistencia su respuesta.		   #
#	Este procedimiento tambien se encarga de registrar #
#	una respuesta a otra respuesta dada al comentario  #
#	en forma de arbol.				   #
############################################################
def responderComentario(request):
    datosRespuesta =  request.raw_post_data
    tree = xml.fromstring(datosRespuesta)  
    for i in tree.iter(): 
	if i.tag == "nickName":
	        nickName = i.text
	elif i.tag == "usuarioRespuesta":
		usuarioRespuesta = i.text
	elif i.tag == "idComentario":
		idComentario = i.text
	elif i.tag == "texto":
		texto = i.text
	elif i.tag == "admiteRespuesta":
		admiteRespuesta = i.text
	elif i.tag == "token":
		token = i.text

    now = datetime.datetime.now()
    elComentario = GestionComentario.Comentario()
    elComentario.nickName = nickName
    elComentario.usuarioRespuesta = usuarioRespuesta
    elComentario.idComentario = idComentario
    elComentario.texto = texto
    elComentario.admiteRespuesta = admiteRespuesta
    elComentario.token = token
    elComentario.fecha = str (now)
    
    usuario = GestionComentario.validarUsuarioRespuesta(idComentario)

    elToken = GestionToken.Token()
    ip = str(request.META['REMOTE_ADDR']) 
    elToken.token = token
    elToken.nickName = nickName
    elToken.ip = ip
  
    if(usuario == usuarioRespuesta):
        if elToken.validarToken() == "TRUE":
	     if GestionComentario.admitirRespuesta(idComentario) == "TRUE":
	         if elComentario.responderComentario() == "TRUE":
	             elComentario.notificarRespuestaComentario(usuarioRespuesta)	
		     return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Se ha agregado satisfactoriamente la respuesta el dia: "+elComentario.fecha},mimetype='application/xml')
		 else:
		     logging.error('EC-015:Error al tratar de generar la respuesta por el usuario '+nickName)
		     return render_to_response('errorMensaje.xml', {'errorMensaje': "Error al tratar de generar la respuesta el dia:" +elComentario.fecha},mimetype='application/xml')
	     else:
	        return render_to_response('errorMensaje.xml', {'errorMensaje': "Este comentario no admite respuesta"},mimetype='application/xml')
        elif elToken.validarToken() == "Error":
	    logging.error('EC-016:Error el tiempo del token del usurario '+nickName+' ha expirado')
	    return render_to_response('errorMensaje.xml', {'errorMensaje': "Lo sentimos el tiempo de su token ha expirado. Vuelva a Iniciar Sesion"},mimetype='application/xml')
            		
        else:
	    logging.error('EC-017:Error el usuario '+nickName+ ' envio un token incorrecto')
	    return render_to_response('errorMensaje.xml', {'errorMensaje': "Error el token enviado es incorrecto"},mimetype='application/xml')
    else:
	logging.error('EC-018:Error la respuesta enviado por el usuario '+nickName+ ' no esta asociada al comentario')
        return render_to_response('errorMensaje.xml', {'errorMensaje': "La respuesta no esta asociada al comentario"},mimetype='application/xml')
	

############################################################
#-------------------- Lista  Comentario--------------------#
#	Se encarga de listar todos los comentarios	   #
#	mas no las respuestas, de un usuario en espe-	   #
#	cifico. Este procedimiento, si la respuesta es     #
#	satisfactoria, retorna todos los datos de los      #
#       comentarios asociados al nickName dado.		   #
############################################################
def listarComentario(request,nickName):

    nickName = str (nickName)
    elComentario = GestionComentario.Comentario()
    listaDeComentarios = GestionComentario.listaComentario(nickName)
	
    if  listaDeComentarios == "FALSE":	
        return render_to_response('errorMensaje.xml', {'errorMensaje': "Error no se encuentran comentarios para esta persona"},mimetype='application/xml')
    else:
        datos = "<listaComentario>"
    	i = 0
        while i < len(listaDeComentarios):
            valores = listaDeComentarios[i].split(':')
	    subetiqueta = "\n     <Comentario>"
	    identificador = "\n     <idComentario>"+valores[0]+"</idComentario>"
	    usuario = "\n     <nickName>"+valores[1]+"</nickName>"
	    texto = "\n     <texto>"+valores[2]+"</texto>"
	    token = "\n     <token>"+valores[3]+"</token>"
	    meGusta = "\n     <meGusta>"+valores[4]+"</meGusta>"
	    noMeGusta = "\n     <noMeGusta>"+valores[5]+"</noMeGusta>"
	    subetiqueta2 = "\n     </Comentario>"
	    datos = datos + subetiqueta+ identificador + usuario + texto + token + meGusta + noMeGusta + subetiqueta2
	    i = i + 1
	datos = datos + "\n</listaComentario>"
	return HttpResponse(datos, content_type= "application/xml")

############################################################
#-------------------- Listar  Respuesta--------------------#
#	Procedimiento que se encarga de listar		   #
#	las respuestas dadas a un comentario en		   #
#	especifico, se muestra el arbol de respuestas	   #
#	segun su jerarquia.				   #
############################################################
def listarRespuesta(request):

    datosRespuesta =  request.raw_post_data
    tree = xml.fromstring(datosRespuesta)
  
    for i in tree.iter(): 
        if i.tag == "nickName":
	    nickName = i.text
	elif i.tag == "idComentario":
	    idComentario = i.text

    laRespuesta = GestionComentario.Comentario()
    listaDeRespuestas = GestionComentario.listaRespuesta(nickName,idComentario)
    if listaDeRespuestas == "FALSE":	
        return render_to_response('errorMensaje.xml', {'errorMensaje': "Error no se encuentran respuestas para esta persona"},mimetype='application/xml')
    else:
        datos = "<listaRespuesta>"
    	i = 0
        while i < len(listaDeRespuestas):
	    valores = listaDeRespuestas[i].split(':')
	    usuario = "\n     <nickName>"+valores[0]+"</nickName>"		
	    usuarioResp = "\n     <usuarioRespuesta>"+valores[1]+"</usuarioRespuesta>"
	    texto = "\n     <texto>"+valores[2]+"</texto>\n"
            datos = datos + usuario + usuarioResp + texto
	    i = i + 1
	datos = datos + "\n</listaRespuesta>"
	return HttpResponse(datos, content_type= "application/xml")

############################################################
#------------------------ Me Gusta-------------------------#
#	Procedimiento que agrega un punto a un 		   #
#	comentario en cuanto a aceptacion o no,		   #
# 	sumando me gusta o no me gusta al mismo.	   #
#       Se valida que solamente se puede sumar me gusta    #
#       o no me gusta, una sola vez por	usuario, 	   #
#	y en tal caso que este lo intente        	   #
#	el procedimiento envia un mensaje de error	   #
#	indicando que la operacion resulto fallida	   #
############################################################
def meGusta(request):

    datosComentario =  request.raw_post_data
    tree = xml.fromstring(datosComentario)  
    for i in tree.iter(): 
        if i.tag == "idComentario":
            idComentario = i.text
	elif i.tag == "nickName":
            nickName = i.text
	elif i.tag == "token":
	    token = i.text
	elif i.tag == "gusto":
	    gusto = i.text

    elComentario = GestionComentario.Comentario()
    elComentario.nickName = nickName
    elComentario.idComentario = idComentario
    elToken = GestionToken.Token()
    ip = str(request.META['REMOTE_ADDR']) 
    elToken.token = token
    elToken.nickName = nickName
    elToken.ip = ip
    if(elComentario.ValidarComentario(idComentario)=='TRUE'):
        if elToken.validarToken() == "TRUE":
	    if(gusto=='TRUE'):#me gusta
                if(elComentario.ponerMeGusta()=="TRUE"):
		    return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Se ha Agregado un 'Me Gusta' al comentario satisfactoriamente"},mimetype='application/xml')
		elif(elComentario.ponerMeGusta()=="FALSE"):
		    logging.error('EC-019:Error no se puede colocar Me Gusta al comentario: '+elComentario.idComentario+ ' otra vez')
		    return render_to_response('errorMensaje.xml', {'errorMensaje': "No se puede colocar 'Me Gusta' a este comentario otra vez"},mimetype='application/xml')
		else:
		    return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "El cambio de 'No Me Gusta' a 'Me Gusta' ha sido exitoso"},mimetype='application/xml')
	    else:#no me gusta
	        if(elComentario.ponerNoMeGusta()=="TRUE"):
		    return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Se ha Agregado un 'No Me Gusta' al comentario satisfactoriamente"},mimetype='application/xml')
		elif(elComentario.ponerNoMeGusta()=="FALSE"):
		    logging.error('EC-020:Error no se puede colocar No Me Gusta al comentario: '+elComentario.idComentario+ ' otra vez')
		    return render_to_response('errorMensaje.xml', {'errorMensaje': "No se puede colocar 'No Me Gusta' a este comentario otra vez"},mimetype='application/xml')
		else:
		    return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "El cambio de 'Me Gusta' a 'No Me Gusta' ha sido exitoso"},mimetype='application/xml')
        elif elToken.validarToken()=="Error":
	    logging.error('EC-021:Error el tiempo del token del usurario '+nickName+' ha expirado')
	    return render_to_response('errorMensaje.xml', {'errorMensaje': "Lo sentimos el tiempo de su token ha expirado. Vuelva a Iniciar Sesion"},mimetype='application/xml')
	else:
	    logging.error('EC-022:Error el usuario '+nickName+ ' envio un token incorrecto')
	    return render_to_response('errorMensaje.xml', {'errorMensaje': "Error el token enviado es incorrecto"},mimetype='application/xml')
    else:
	logging.error('EC-023:Error el comentario: '+elComentario.idComentario+ ' no existe')
        return render_to_response('errorMensaje.xml', {'errorMensaje': "Error el comentario no existe"},mimetype='application/xml') 


############################################################
#----------------- Eliminar Comentario --------------------#
#	Procedimiento que permite eliminar un comentario   #
#	validando que unicamente el creador del mismo	   #
#	es quien esta ejecutando dicha operacion	   #
############################################################
def eliminarComentarios(request):

    datosComentario =  request.raw_post_data
    tree = xml.fromstring(datosComentario)  
    for i in tree.iter(): 
	if i.tag == "nickName":
	    nickName = i.text
	elif i.tag == "idComentario":
	    idComentario = i.text
	elif i.tag == "token":
	    token = i.text
	
    elComentario = GestionComentario.Comentario()
    elComentario.nickName = nickName
    elComentario.idComentario = idComentario

    elToken = GestionToken.Token()
    ip = str(request.META['REMOTE_ADDR']) 
    elToken.token = token
    elToken.nickName = nickName
    elToken.ip = ip
  
    if elToken.validarToken() == "TRUE":
    	if (elComentario.eliminarComentario(idComentario)=="TRUE"):
	    return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Se ha eliminado el comentario satisfactoriamente"},mimetype='application/xml')
	elif (elComentario.eliminarComentario(idComentario)=="Error"):
	    logging.error('EC-024:Error '+nickName+ ' no es un usuario autorizado para eliminar el comentario '+elComentario.idComentario)
	    return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Ud no es un usuario autorizado para eliminar este comentario"},mimetype='application/xml')
	else:
	    logging.error('EC-025:Error el comentario '+elComentario.idComentario+' no existe')
	    return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Error el comentario a eliminar no existe"},mimetype='application/xml')
    elif elToken.validarToken()=="Error":
	logging.error('EC-026:Error el tiempo del token del usurario '+nickName+' ha expirado')
        return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Lo sentimos el tiempo de su token ha expirado. Vuelva a Iniciar Sesion"},mimetype='application/xml')
    else:
	logging.error('EC-027:Error el usuario '+nickName+ ' envio un token incorrecto')
	return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Error el token enviado es incorrecto"},mimetype='application/xml')

############################################################
#----------------- Listar Etiqueta ------------------------#
#	Procedimiento que se encarga de listar		   #
#	los datos de comentarios que contengan		   #
#	la etiqueta solicitada via URL en el request	   #
#	que se comunica a la vista y esta llama 	   #
#	a dicha rutina para que retorne los datos buscados #
#	para luego buscar el comentario y mostrar sus      #
#	datos con un HttpResponse en formato xml	   #  
############################################################

def listarEtiqueta(request,nombreEtiqueta):
    listaDeDatosComentario = GestionComentario.listaEtiquetas(nombreEtiqueta)
    if  listaDeDatosComentario == "FALSE":
        return render_to_response('errorMensaje.xml', {'errorMensaje': "Error no se encuentran comentarios con esta etiqueta"},mimetype='application/xml')
    else:
        datos = "<listaComentariosConEtiquetas>\n"
    	i = 0
	losComentarios = ''
	resultado = ''
        while i < len(listaDeDatosComentario):
	    valores = listaDeDatosComentario[i].split(':')
	    idComentario = valores[0]		
	    nickName = valores[1]
	    losComentarios = losComentarios + GestionComentario.listarComentariosConEtiqueta(idComentario,nickName) 
	    i = i + 1
	i = 0
	arreglo = losComentarios.split(":")
	while i < len(arreglo)-1:
	    resultado = resultado + "<texto>" + arreglo[i] + "<texto>\n"
   	    i = i + 1

	datos = datos + resultado + "</listaComentariosConEtiquetas>"
	return HttpResponse(datos, content_type= "application/xml")

############################################################
#-----------------------Cuenta me gusta--------------------#
#	Procedimiento que retorna un entero con el 	   #
#	contador de registros que indican que le gusta	   #
#	un comentario a un usuario			   #
############################################################

def cuentaMeGusta(request):

    datosComentario =  request.raw_post_data
    tree = xml.fromstring(datosComentario)  
    for i in tree.iter(): 
        if i.tag == "idComentario":
	    idComentario = i.text

    contador = GestionComentario.contarMeGusta(idComentario)
    if (contador == "FALSE"):
	logging.error('EC-028:Error el comentario '+idComentario+' no existe')
	return render_to_response('errorMensaje.xml', {'errorMensaje': "Este comentario no existe"},mimetype='application/xml')
    else:
	return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "A "+ str(contador) + " Personas le(s) gusta este comentario "},mimetype='application/xml')


############################################################
#--------------------Cuenta no me gusta--------------------#
#	Procedimiento que retorna un entero con el 	   #
#	contador de registros que indican que no le gusta  #
#	un comentario a un usuario			   #
############################################################
def cuentaNoMeGusta(request):

    datosComentario = request.raw_post_data
    tree = xml.fromstring(datosComentario)  
    for i in tree.iter(): 
        if i.tag == "idComentario":
	    idComentario = i.text
	
    contador = GestionComentario.contarNoMeGusta(idComentario)
    if (contador == "FALSE"):
	logging.error('EC-029:Error el comentario '+idComentario+' no existe')
	return render_to_response('errorMensaje.xml', {'errorMensaje': "Este comentario no existe"},mimetype='application/xml')
    else:
	return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "A "+ str(contador) + " Personas NO le(s) gusta este comentario "},mimetype='application/xml')
