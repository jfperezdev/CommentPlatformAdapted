from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
import xml.etree.ElementTree as xml
import collections
import misitio.models.Usuario

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
    
    elUsuario = misitio.models.Usuario.Usuario(nickName
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


