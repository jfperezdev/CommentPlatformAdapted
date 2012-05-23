#*********************************************************************************************
#                      Archivo: viewsUsuario.py
#                      -------------------
#   copyright            : (C) 2012 by Developer Group: Jose Francisco
#							de Jesus Perez Vera
#                                                       Armen Djenanian Dertorossian
#							Kristian Cortes
# ********************************************************************************************
# PlatformCommentAdapter. Proyecto de Desarrollo del Software
# ********************************************************************************************
# Descripcion : Archivo que contiene la vista Usuario
# ********************************************************************************************
from django.http import HttpResponse
from django.http import HttpRequest
from django.shortcuts import render_to_response
import xml.etree.ElementTree as xml
import misitio.models.Usuario as GestionUsuario
import misitio.models.Token as GestionToken
import datetime
import time

############################################################
#----------------- Registrar Usuario-----------------------#
#	Procedimiento encargado de registrar a un usuario  #
#	a partir de un request en formato XML, pasandolo   #
# 	a una cadena de caracteres e insertandolo en la    #
#	base de datos.                                     #
############################################################
def registrarUsuario(request):
    datosUsuario =  request.raw_post_data
    tree = xml.fromstring(datosUsuario)
    
    for i in tree.iter(): 
        if i.tag == "nickName":
	    nickName = i.text
	elif i.tag == "password":
	    password = i.text
	elif i.tag == "primerNombre":
	    primerNombre = i.text
	elif i.tag == "segundoNombre":
	    segundoNombre = i.text
	elif i.tag == "primerApellido":
	    primerApellido = i.text
	elif i.tag == "segundoApellido":
	    segundoApellido = i.text
	elif i.tag == "email":
	    email = i.text
	elif i.tag == "fechaNacimiento":
	    fechaNacimiento = i.text
	elif i.tag == "paisOrigen":
	    paisOrigen = i.text
	elif i.tag == "biografia":
	    biografia = i.text
	elif i.tag == "foto":
	    foto = i.text
    
    elUsuario = GestionUsuario.Usuario()
    elUsuario.nickName = nickName
    elUsuario.password = password
    elUsuario.primerNombre = primerNombre
    elUsuario.segundoNombre = segundoNombre
    elUsuario.primerApellido = primerApellido
    elUsuario.segundoApellido = segundoApellido
    elUsuario.email = email
    elUsuario.fechaNacimiento = fechaNacimiento
    elUsuario.paisOrigen = paisOrigen
    elUsuario.biografia = biografia
    elUsuario.foto = foto 
    
    if elUsuario.registrarse() == "TRUE":	
        return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Se ha agregado satisfactoriamente el usuario "+elUsuario.nickName},mimetype='application/xml')
    elif elUsuario.registrarse() == "Error":
        return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "El usuario "+elUsuario.nickName+" ya se encuentra registrado"},mimetype='application/xml')
    else:
	return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Error al tratar de registrar al usuario "+elUsuario.nickName},mimetype='application/xml')

############################################################
#----------------- Modificar Usuario-----------------------#
#	Procedimiento encargado de modificar a un usuario  #
#	a partir de un request en formato XML, pasandolo   #
# 	a una cadena de caracteres e insertandolo en la    #
#	base de datos con los datos nuevos.                #
############################################################
def modificarUsuario(request):
    datosUsuario =  request.raw_post_data
    tree = xml.fromstring(datosUsuario)
    
    for i in tree.iter(): 
	if i.tag == "nickName":
	    nickName = i.text
	elif i.tag == "password":
	    password = i.text
	elif i.tag == "primerNombre":
	    primerNombre = i.text
	elif i.tag == "segundoNombre":
	    segundoNombre = i.text
	elif i.tag == "primerApellido":
	    primerApellido = i.text
	elif i.tag == "segundoApellido":
	    segundoApellido = i.text
	elif i.tag == "email":
	    email = i.text
	elif i.tag == "fechaNacimiento":
	    fechaNacimiento = i.text
	elif i.tag == "paisOrigen":
	    paisOrigen = i.text
	elif i.tag == "biografia":
	    biografia = i.text
	elif i.tag == "foto":
	    foto = i.text
	elif i.tag == "token":
	    token = i.text
    
    elUsuario = GestionUsuario.Usuario()
    elUsuario.nickName = nickName
    elUsuario.password = password
    elUsuario.primerNombre = primerNombre
    elUsuario.segundoNombre = segundoNombre
    elUsuario.primerApellido = primerApellido
    elUsuario.segundoApellido = segundoApellido
    elUsuario.email = email
    elUsuario.fechaNacimiento = fechaNacimiento
    elUsuario.paisOrigen = paisOrigen
    elUsuario.biografia = biografia
    elUsuario.foto = foto

    elToken = GestionToken.Token()
    ip = str(request.META['REMOTE_ADDR']) 
    elToken.token = token
    elToken.nickName = nickName
    elToken.ip = ip
    miToken = elToken.validarToken()
  
    if miToken == "TRUE":
        if elUsuario.modificarse() == "TRUE":	
       	    return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Se ha modificado satisfactoriamente el usuario "+elUsuario.nickName},mimetype='application/xml')
	else:
       	    return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Error al tratar de modificar al usuario "+elUsuario.nickName},mimetype='application/xml')
    elif miToken == "Error":
	return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Lo sentimos el tiempo de su token ha expirado. Vuelva a Iniciar Sesion"},mimetype='application/xml')
    else:
	return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Error el token enviado es incorrecto"},mimetype='application/xml')
	
############################################################
#-------------------- Iniciar Sesion-----------------------#
#	Procedimiento encargado de iniciar sesion usuario  #
#	a partir de un request en formato XML, pasandolo   #
# 	a una cadena de caracteres y validando la informa- #
#	cion en la base de datos.                          #
#	Si el usuario tiene un token vigente, quiere	   #
#	decir que tiene iniciada una sesion para ese IP    #
#	desde donde accede. En tal caso que quiera iniciar #
#	sesion y cuente con un token vigente, el sistema   #
#	rechazara la peticion y le explicara lo dicho.	   #
#	En tal caso que no tenga un token vigente en esa   #
#	ip entonces el sistema le retornara su token       #
#	con el que podra consumir los recursos que lo	   #
#	requieren en el sistema.			   #
############################################################

def iniciarSesion(request):
    datosUsuario =  request.raw_post_data
    tree = xml.fromstring(datosUsuario)
    ip = str(request.META['REMOTE_ADDR'])
    for i in tree.iter(): 
	if i.tag == "nickName":
	    nickName = i.text
	elif i.tag == "password":
	    password = i.text

    elUsuario = GestionUsuario.Usuario()
    elUsuario.nickName = nickName
    elUsuario.password = password

    esUsuarioValido = elUsuario.validarSesion(nickName)
    elToken = GestionToken.Token()
    elToken.nickName = nickName
    elToken.ip = ip
    tieneToken = elToken.tieneToken()
    	
    if (esUsuarioValido == "TRUE" and  tieneToken == "FALSE"):
        now = datetime.datetime.now()
	miToken = elToken.insertarToken()
        if(miToken != "FALSE"):
	    return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Se ha iniciado sesion satisfactoriamente con su cuenta. Su token es:" + miToken},mimetype='application/xml')
	else:	
	    return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Error no se ha podido crear el Token"},mimetype='application/xml')
	    	
    elif esUsuarioValido == "FALSE":
	return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Error, verifique su nickName y password"},
	mimetype='application/xml')
    elif (esUsuarioValido == "TRUE" and tieneToken == "TRUE"):
	return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Error, " + nickName +" aun tiene un token valido"},
	mimetype='application/xml')

############################################################
#------------------ Eliminar Usuario ----------------------#
#	Procedimiento que permite eliminar a un usuario    #
#	cuyo nickName, password y token sean validos.      #
#	Una vez confirmada la operacion el usuario es      #
#	borrado automaticamente de la BD llamando a 	   #
#       un procedimiento en el models que se encarga de    #
#	dicha operacion.				   #
############################################################
def eliminarUsuario(request):
    datosEliminarUsuario = request.raw_post_data
    tree = xml.fromstring(datosEliminarUsuario)
    ip = str(request.META['REMOTE_ADDR'])
    for i in tree.iter(): 
	if i.tag == "nickName":
	    nickName = i.text
	elif i.tag == "password":
	    password = i.text
	elif i.tag == "token":
	    token = i.text
	
    elUsuario = GestionUsuario.Usuario()
    elUsuario.nickName = nickName
    elUsuario.password = password
    sesionValida = elUsuario.validarSesion(nickName)
    elToken = GestionToken.Token()
    ip = str(request.META['REMOTE_ADDR']) 
    elToken.token = token
    elToken.nickName = nickName
    elToken.ip = ip
    	
    if (sesionValida == "TRUE"):
        if elToken.validarToken() == "TRUE":
	    if elUsuario.eliminarUsuario() == "TRUE":
	        return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Se ha eliminado su cuenta satisfactoriamente"}, mimetype='application/xml')
	    else:
	        return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Error, verifique su nickname y password"}, mimetype='application/xml')
        else:
	    return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Error el token enviado es incorrecto"},mimetype='application/xml')
    else:
         return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Error, verifique su nickName y password"},mimetype='application/xml')
