from django.http import HttpResponse
from django.shortcuts import render_to_response
from pycassa.pool import ConnectionPool
from pycassa.columnfamily import ColumnFamily
from django.shortcuts import render
import xml.etree.ElementTree as xml
import datetime
import pycassa
import collections

def usuariosRegistrados(request):
    pool = ConnectionPool('baseDeDatos')
    if pool:print 'se conecto!'
    else: print 'no se conecta'
    col_fam = pycassa.ColumnFamily(pool, 'Tabla')
    columna = col_fam.get('5',columns=['nombre'])
    columna = columna['nombre']
    return render_to_response('retornarUsuariosRegistrados.xml', {'datosUsuarios': columna}, mimetype='application/xml')
 
def enviarXml(request): 
    dato =  request.raw_post_data
    tree = xml.fromstring(dato)
    for node in tree.iter("nombre"):
	print "%s" %node.text
    return render_to_response('retornarUsuariosRegistrados.xml', {'datosUsuarios': node.text}, mimetype='application/xml')

def registrarUsuario(request):
    datosUsuario =  request.raw_post_data
    tree = xml.fromstring(datosUsuario)
    pool = ConnectionPool('baseDeDatos')
    col_fam = pycassa.ColumnFamily(pool, 'Tabla')
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
	
    col_fam.insert (nickName, {'password': password
    ,'primerNombre': primerNombre
    ,'segundoNombre': segundoNombre
    ,'primerApellido': primerApellido
    ,'segundoApellido': segundoApellido
    ,'email': email
    ,'fechaNacimiento': fechaNacimiento
    ,'paisOrigen': paisOrigen
    ,'biografia': biografia
    ,'foto': foto})
    
    return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Se ha agregado satisfactoriamente el usuario "+nickName},
    mimetype='application/xml')

def iniciarSesion(request):
    
    datosUsuario =  request.raw_post_data
    tree = xml.fromstring(datosUsuario)
    pool = ConnectionPool('baseDeDatos')
    col_fam = pycassa.ColumnFamily(pool, 'Tabla')
    for i in tree.iter():
	if i.tag == "nickName":
	        nickName = i.text
	elif i.tag == "password":
		password = i.text

    resultado = col_fam.get(nickName, columns=['password'])
    usuario = resultado['nickName']
    clave = resultado['password']

   if(nickName == usuario) and (clave == password)
	return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "true"},
    	mimetype='application/xml')
   else
	return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "false"},
    	mimetype='application/xml')
