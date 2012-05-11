from django.http import HttpResponse
from django.shortcuts import render_to_response
import xml.etree.ElementTree as xml
import misitio.models.Comentario as GestionComentario
import misitio.models.Token as GestionToken
import datetime
import pycassa
from pycassa.pool import ConnectionPool
from pycassa.columnfamily import ColumnFamily

############################################################
#----------------- Registrar Comentario--------------------#
def registrarComentario(request):

    datosComentario =  request.raw_post_data
    tree = xml.fromstring(datosComentario)  
    for i in tree.iter(): 
	if i.tag == "nickName":
	        nickName = i.text
	elif i.tag == "texto":
		texto = i.text
	elif i.tag == "adjunto":
		adjunto = i.text
	elif i.tag == "token":
		token = i.text
	elif i.tag == "admiteRespuesta":
		admiteRespuesta = i.text
    now = datetime.datetime.now()

    elComentario = GestionComentario.Comentario()
    elComentario.nickName = nickName
    elComentario.texto = texto
    elComentario.adjunto = adjunto
    elComentario.token = token
    elComentario.admiteRespuesta = admiteRespuesta
    elComentario.fecha = str (now)

    elToken = GestionToken.Token()
    ip = str(request.META['REMOTE_ADDR']) 
    elToken.token = token
    elToken.nickName = nickName
    elToken.ip = ip
  
    if elToken.validarToken() == "TRUE":
    	if elComentario.registrarComentario() == "TRUE":	
       		return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Se ha agregado satisfactoriamente el Comentario el dia: "+elComentario.fecha},mimetype='application/xml')
	else:
       	        return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Error al tratar de generar el Comentario el dia:" +elComentario.fecha},mimetype='application/xml')
    elif elToken.validarToken()=="Error":
	 return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Lo sentimos el tiempo de su token ha expirado. Vuelva a Iniciar Sesion"},mimetype='application/xml')
    else:
	return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Error el token enviado es incorrecto"},mimetype='application/xml')
	



############################################################
#----------------- Responder Comentario--------------------#
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
	elif i.tag == "adjunto":
		adjunto = i.text
	elif i.tag == "token":
		token = i.text
    now = datetime.datetime.now()

    elComentario = GestionComentario.Comentario()
    elComentario.nickName = nickName
    elComentario.usuarioRespuesta = usuarioRespuesta
    elComentario.idComentario = idComentario
    elComentario.texto = texto
    elComentario.adjunto = adjunto
    elComentario.token = token
    elComentario.fecha = str (now)
   
    pool = ConnectionPool('baseDeDatos')
    col_fam = pycassa.ColumnFamily(pool, 'Comentario') 
    resultado = col_fam.get(idComentario,columns=['nickName']) 
    usuario = resultado['nickName']

    elToken = GestionToken.Token()
    ip = str(request.META['REMOTE_ADDR']) 
    elToken.token = token
    elToken.nickName = nickName
    elToken.ip = ip
  
    if(usuario == usuarioRespuesta):
	    if elToken.validarToken() == "TRUE":
			if  elComentario.admitirRespuesta(idComentario) == "TRUE":
			    	if elComentario.responderComentario() == "TRUE":	
			       	   return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Se ha agregado satisfactoriamente la respuesta el dia: "+elComentario.fecha},mimetype='application/xml')
				else:
			       	   return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Error al tratar de generar la respuesta el dia:" +elComentario.fecha},mimetype='application/xml')
			else:
				 return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Este comentario no admite respuesta"},mimetype='application/xml')
            elif elToken.validarToken() == "Error":
		 return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Lo sentimos el tiempo de su token ha expirado. Vuelva a Iniciar Sesion"},mimetype='application/xml')
            		
	    else:
		return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Error el token enviado es incorrecto"},mimetype='application/xml')
    else:
	  return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "La respuesta no esta asociada al comentario"},mimetype='application/xml')


############################################################
#-------------------- Lista  Comentario--------------------#
def listarComentario(request,nickName):

    nickName = str (nickName)
    elComentario = GestionComentario.Comentario()
    listaDeComentarios = GestionComentario.listaComentario(nickName)
	
    if  listaDeComentarios == "FALSE":	
	   return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Error no se encuentran comentarios para esta persona"},mimetype='application/xml')
    else:
	  datos = " "
    	  i = 0
          while i < len(listaDeComentarios):
	    	valores = listaDeComentarios[i].split(':')
		usuario = "<nickName>"+valores[0]+"</nickName>"
		texto = "<texto>"+valores[1]+"</texto>"
		token = "<token>"+valores[2]+"</token>"
		adjunto = "<adjunto>"+valores[3]+"</adjunto>"
		datos = datos + usuario + texto + token + adjunto
		i = i + 1
		  	        
	  return render_to_response('listarComentarios.xml', {'datos':datos}, mimetype='application/xml')

############################################################
#-------------------- Listar  Respuesta--------------------#
def listarRespuesta(request,usuarioRespuesta):

    nickName = str (nickName)
    laRespuesta = GestionComentario.Comentario()
    listaDeRespuestas = GestionComentario.listaRespuesta(usuarioRespuesta)
    if  listaDeComentarios == "FALSE":	
	   return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Error no se encuentran respuestas para esta persona"},mimetype='application/xml')
    else:
	  datos = " "
    	  i = 0
          while i < len(listaDeRespuestas):
	    	valores = listaDeRespuestas[i].split(':')
		usuario = "<nickName>"+valores[0]+"</nickName>\n"		
		usuarioResp = "<usuarioRespuesta>"+valores[1]+"</usuarioRespuesta>\n"
		texto = "<texto>"+valores[2]+"</texto>\n"
		token = "<token>"+valores[3]+"</token>\n"
		adjunto = "<adjunto>"+valores[4]+"</adjunto>\n"
		datos = datos + usuario + usuarioResp + texto + token + adjunto
		i = i + 1
	  return render_to_response('listarComentarios.xml', {'datos':datos}, mimetype='application/xml')

#def varlidarHashTag(request):
#	
#	comentario = comentario + ' '
#	arreglo = comentario.split(' ')
#	i = 0
#	while (i < len(arreglo) - 1):
 #  	   if not arreglo[i].find("#"):
#		print arreglo[i]


############################################################
#-------------------- Me Gusta--------------------#
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

    elComentario = GestionComentario.Comentario()
    elComentario.nickName = nickName
    elComentario.idComentario = idComentario

    elToken = GestionToken.Token()
    ip = str(request.META['REMOTE_ADDR']) 
    elToken.token = token
    elToken.nickName = nickName
    elToken.ip = ip
  
    if elToken.validarToken() == "TRUE":
    	if(elComentario.ponerMeGusta()=="TRUE"):
		return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Se a Agregado un Megusta al comentario satisfactoriamente"},mimetype='application/xml')
	else:
		return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Nose puede colocar me gusta a este comentario"},mimetype='application/xml')
    elif elToken.validarToken()=="Error":
	 return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Lo sentimos el tiempo de su token ha expirado. Vuelva a Iniciar Sesion"},mimetype='application/xml')
    else:
	return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Error el token enviado es incorrecto"},mimetype='application/xml')
	

