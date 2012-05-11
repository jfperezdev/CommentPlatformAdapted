from django.http import HttpResponse
from django.http import HttpRequest
from django.shortcuts import render_to_response
import xml.etree.ElementTree as xml
import misitio.models.Usuario as GestionUsuario
import misitio.models.Token as GestionToken
import datetime
import time
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
  
    if elToken.validarToken() == "TRUE":
    	if elUsuario.modificarse() == "TRUE":	
       		return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Se ha modificado satisfactoriamente el usuario "+elUsuario.nickName},
	    mimetype='application/xml')
	else:
       	        return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Error al tratar de modificar al usuario "+elUsuario.nickName},
	    mimetype='application/xml')
    elif elToken.validarToken()=="Error":
	 return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Lo sentimos el tiempo de su token ha expirado. Vuelva a Iniciar Sesion"},mimetype='application/xml')
    else:
	return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Error el token enviado es incorrecto"},mimetype='application/xml')
	
   

def generarIdToken():
		vacio = True
		cont = 0
		try:
			pool = ConnectionPool('baseDeDatos')
			col_fam = pycassa.ColumnFamily(pool,'Token')
			resultado = col_fam.get_range(column_start='accion', column_finish='nickName')
			arreglo = []

			for key,columns in resultado:
				arreglo.append(key)
				cont = cont+1
				vacio = False

			

		except Exception:
		     return "FALSE"
		else:
		     if vacio == True:
			return '1'
		     else:
		        nuevoId = unicode(cont+1)
		        return nuevoId





def validarUsuarioIp(nickName, ip):
	     try:
		    
	    	    pool = ConnectionPool('baseDeDatos')
	    	    col_fam = pycassa.ColumnFamily(pool, 'Token')
		    resultado = col_fam.get_range(column_start='accion', column_finish='nickName')
		    arreglo = []
		    
		    for key,columns in resultado:
			 
                    	nickName2 = columns['nickName']
                    	ip2 = columns ['ip']
		        nowToken = columns ['fecha']
						

		    	if (nickName2==nickName) and(ip2 == ip):

				   nowToken2 = columns['fecha'].split(".")
			    	   nowToken = datetime.datetime(*time.strptime(nowToken2[0],'%Y-%m-%d %H:%M:%S')[0:6])
				   now = datetime.datetime.now()
			    	   diferenciaToken = now - nowToken
				   horas = str(diferenciaToken).split(":")	   
				   minutos = int(horas[1])
				   
				   if (horas[0]=="0") and (minutos<=4):
				   	return "FALSE"
			
		    return "TRUE"
             except Exception:
		return "FALSE"
	     else:
		return "TRUE"

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

#   elToken = GestionToken.Token()
 #  resp = elToken.validarUsuarioIp(nickName,ip)
    resp = validarUsuarioIp(nickName,ip)
    	
    if (respuesta == "TRUE"):
    	    if(resp == "TRUE"):
		now = datetime.datetime.now()
		pool = ConnectionPool('baseDeDatos')	
		col_fam = pycassa.ColumnFamily(pool, 'Token')
		elId = generarIdToken()	
		col_fam.insert (elId, {'ip': ip,'fecha': str(now) ,'nickName': nickName, 'accion': 'Generar Token', 'idToken': elId})
		return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Se ha iniciado sesion satisfactoriamente con su cuenta. Su token es:" + elId},mimetype='application/xml')
	    else:
		
		return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Error el usuario tiene un token vigente"},mimetype='application/xml')
	    	
    else:
		return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Error, verifique su nickName y password"},
	mimetype='application/xml')

	    	


