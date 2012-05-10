from django.http import HttpResponse
from django.http import HttpRequest
from django.shortcuts import render_to_response
import xml.etree.ElementTree as xml
import misitio.models.Usuario as GestionUsuario
import datetime
import pycassa
from pycassa.pool import ConnectionPool
from pycassa.columnfamily import ColumnFamily

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
    
	
    if elUsuario.modificarse() == "TRUE":	
	    return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Se ha modificado satisfactoriamente el usuario "+elUsuario.nickName},
	    mimetype='application/xml')
    else:
	    return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Error al tratar de modificar al usuario "+elUsuario.nickName},
	    mimetype='application/xml')


def generarIdToken():
		vacio = True
		try:
			pool = ConnectionPool('baseDeDatos')
			col_fam = pycassa.ColumnFamily(pool,'Token')
			resultado = col_fam.get_range(column_start='fecha', column_finish='nickName')
			arreglo.range(900)

			for key,columns in resultado:
				arreglo.append(key)
				vacio = False

			listaIdToken = sorted(arreglo,reverse=True)

		except Exception:
		     return "FALSE"
		else:
		     if vacio == True:
			return '1'
		     else:
		        nuevoId = str(int(listaIdToken[0]) + 10)
		        return nuevoId

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
    ip = str(request.META['REMOTE_ADDR'])
    for i in tree.iter(): 
	if i.tag == "nickName":
	        nickName = i.text
	elif i.tag == "password":
		password = i.text

    elUsuario = GestionUsuario.Usuario()
    elUsuario.nickName = nickName
    elUsuario.password = password

    respuesta = elUsuario.validarSesion(nickName)

    if respuesta == 'TRUE':
	now = datetime.datetime.now()
	pool = ConnectionPool('baseDeDatos')
	col_fam = pycassa.ColumnFamily(pool, 'Token')
	elId = generarIdToken()	
	col_fam.insert (elId, {'ip': ip,'fecha': str(now) ,'nickName': nickName, 'accion': 'Generar Token'})
        return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Se ha iniciado sesion satisfactoriamente con tu cuenta. El token es:" + elId},
mimetype='application/xml')
    else:
	return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Error, el usuario es incorrecto"},
mimetype='application/xml')



