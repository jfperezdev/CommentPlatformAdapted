from django.http import HttpResponse
from django.shortcuts import render_to_response
import xml.etree.ElementTree as xml
import misitio.models.Usuario as GestionUsuario

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
    
    elUsuario = GestionUsuario.Usuario(nickName
    ,password
    ,primerNombre
    ,segundoNombre
    ,primerApellido
    ,segundoApellido
    ,email
    ,fechaNacimiento
    ,paisOrigen
    ,biografia
    ,foto) 
    
	
    if elUsuario.registrarse() == "TRUE":	
	    return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Se ha agregado satisfactoriamente el usuario "+elUsuario.nickName},
	    mimetype='application/xml')
    else:
	    return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Error al tratar de registrar al usuario "+elUsuario.nickName},
	    mimetype='application/xml')
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
    
    elUsuario = GestionUsuario.Usuario(nickName
    ,password
    ,primerNombre
    ,segundoNombre
    ,primerApellido
    ,segundoApellido
    ,email
    ,fechaNacimiento
    ,paisOrigen
    ,biografia
    ,foto) 
    
	
    if elUsuario.modificarse() == "TRUE":	
	    return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Se ha modificado satisfactoriamente el usuario "+elUsuario.nickName},
	    mimetype='application/xml')
    else:
	    return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Error al tratar de modificar al usuario "+elUsuario.nickName},
	    mimetype='application/xml')

############################################################
#-------------------- Iniciar Sesion-----------------------#
#	Procedimiento encargado de iniciar sesion usuario  #
#	a partir de un request en formato XML, pasandolo   #
# 	a una cadena de caracteres y validando la informa- #
#	cion en la base de datos.                          #
############################################################
def iniciarSesion(request):
    datosUsuario =  request.raw_post_data
    tree = xml.fromstring(datosUsuario)
    
    for i in tree.iter(): 
	if i.tag == "nickName":
	        nickName = i.text
	elif i.tag == "password":
		password = i.text

    elUsuario = GestionUsuario.Usuario(nickName,password,"","","","","","","","","")
    if elUsuario.validarSesion(nickName) == "TRUE":
	return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': elUsuario.nickName + ", Se ha iniciado sesion satisfactoriamente con tu cuenta"},
	    mimetype='application/xml')
    else:
	    return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Error al tratar de iniciar sesion con esta cuenta. Pruebe que el usuario existe y que la clave es correcta"},mimetype='application/xml')


