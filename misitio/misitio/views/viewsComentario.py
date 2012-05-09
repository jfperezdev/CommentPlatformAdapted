from django.http import HttpResponse
from django.shortcuts import render_to_response
import xml.etree.ElementTree as xml
import misitio.models.Comentario as GestionComentario
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
    now = datetime.datetime.now()

    elComentario = GestionComentario.Comentario()
    elComentario.nickName = nickName
    elComentario.texto = texto
    elComentario.adjunto = adjunto
    elComentario.token = token
    elComentario.fecha = str (now)
	    
    if elComentario.registrarComentario() == "TRUE":	
       return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Se ha agregado satisfactoriamente el Comentario el dia: "+elComentario.fecha},mimetype='application/xml')
    else:
       return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Error al tratar de generar el Comentario el dia:" +elComentario.fecha},mimetype='application/xml')

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

    if(usuario == usuarioRespuesta):
	    if elComentario.responderComentario() == "TRUE":	
	       return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Se ha agregado satisfactoriamente la respuesta el dia: "+elComentario.fecha},mimetype='application/xml')
    	    else:
	       return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Error al tratar de generar la respuesta el dia:" +elComentario.fecha},mimetype='application/xml')

    else:
	    return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "La respuesta no esta asociada al comentario"},mimetype='application/xml')




#def varlidarHashTag(request):
#	
#	comentario = comentario + ' '
#	arreglo = comentario.split(' ')
#	i = 0
#	while (i < len(arreglo) - 1):
 #  	   if not arreglo[i].find("#"):
#		print arreglo[i]

    		

