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
        elif i.tag == "etiquetas":
	        etiquetas = i.text
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
    	if elComentario.registrarComentario(etiquetas) == "TRUE":	
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
				   elComentario.notificarRespuestaComentario(usuarioRespuesta)	
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
	  datos = "<listaComentario>"
    	  i = 0
          while i < len(listaDeComentarios):
	    	valores = listaDeComentarios[i].split(':')
		usuario = "\n     <nickName>"+valores[0]+"</nickName>"
		texto = "\n     <texto>"+valores[1]+"</texto>"
		token = "\n     <token>"+valores[2]+"</token>"
		adjunto = "\n     <adjunto>"+valores[3]+"</adjunto>\n"
		datos = datos + usuario + texto + token + adjunto
		i = i + 1
	  datos = datos + "\n<listaComentario>"
	  	        
	  return HttpResponse(datos, content_type= "application/xml")

############################################################
#-------------------- Listar  Respuesta--------------------#
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
    if  listaDeRespuestas == "FALSE":	
	   return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Error no se encuentran respuestas para esta persona"},mimetype='application/xml')
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
	  datos = datos + "\n<listaRespuesta>"
	  return HttpResponse(datos, content_type= "application/xml")

############################################################
#------------------------ Me Gusta-------------------------#
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
				return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Se a Agregado un 'Me Gusta' al comentario satisfactoriamente"},mimetype='application/xml')
			elif(elComentario.ponerMeGusta()=="FALSE"):
				return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "No se puede colocar 'Me Gusta' a este comentario otra vez"},mimetype='application/xml')
			else:
				return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "El cambio de 'No Me Gusta' a 'Me Gusta' a sido exitoso"},mimetype='application/xml')
		else:#no me gusta
			if(elComentario.ponerNoMeGusta()=="TRUE"):
				return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Se a Agregado un 'No Me Gusta' al comentario satisfactoriamente"},mimetype='application/xml')
			elif(elComentario.ponerNoMeGusta()=="FALSE"):
				return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "No se puede colocar 'No Me Gusta' a este comentario otra vez"},mimetype='application/xml')
			else:
				return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "El cambio de 'Me Gusta' a 'No Me Gusta' a sido exitoso"},mimetype='application/xml')
	    elif elToken.validarToken()=="Error":
		 return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Lo sentimos el tiempo de su token ha expirado. Vuelva a Iniciar Sesion"},mimetype='application/xml')
	    else:
		return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Error el token enviado es incorrecto"},mimetype='application/xml')
    else:
	return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Error el comentario no existe"},mimetype='application/xml') 


################################################################
#--------------------- Eliminar Comentarios--------------------#
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
    	if(elComentario.eliminarComentario(idComentario)=="TRUE"):
		return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Se ha eliminado el comentario satisfactoriamente"},mimetype='application/xml')
	elif (elComentario.eliminarComentario(idComentario)=="Error"):
		return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Ud no es un usuario autorizado para eliminar este comentario"},mimetype='application/xml')
	else:
		return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Error el comentario a eliminar no existe"},mimetype='application/xml')
    elif elToken.validarToken()=="Error":
	 return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Lo sentimos el tiempo de su token ha expirado. Vuelva a Iniciar Sesion"},mimetype='application/xml')
    else:
	return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Error el token enviado es incorrecto"},mimetype='application/xml')



################################################################
#--------------------- Listar Etiqueta-------------------------#

def listarEtiqueta(request,nombreEtiqueta):
    listaDeDatosComentario = GestionComentario.listaEtiquetas(nombreEtiqueta)
    if  listaDeDatosComentario == "FALSE":
	return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Error no se encuentran comentarios con esta etiqueta"},mimetype='application/xml')
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



################################################################
#---------------------Cuenta me gusta--------------------------#

def cuentaMeGusta(request):

    datosComentario =  request.raw_post_data
    tree = xml.fromstring(datosComentario)  
    for i in tree.iter(): 
	if i.tag == "idComentario":
	        idComentario = i.text

    contador = GestionComentario.contarMeGusta(idComentario)
    if (contador == "FALSE"):
	return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Este comentario no existe"},mimetype='application/xml')
    else:
	return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "A "+ str(contador) + " Personas le(s) gusta este comentario "},mimetype='application/xml')


################################################################
#---------------------Cuenta no me gusta-----------------------#
def cuentaNoMeGusta(request):

    datosComentario =  request.raw_post_data
    tree = xml.fromstring(datosComentario)  
    for i in tree.iter(): 
	if i.tag == "idComentario":
	        idComentario = i.text
	
    contador = GestionComentario.contarNoMeGusta(idComentario)
    if (contador == "FALSE"):
	return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Este comentario no existe"},mimetype='application/xml')
    else:
	return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "A "+ str(contador) + " Personas NO le(s) gusta este comentario "},mimetype='application/xml')
	








