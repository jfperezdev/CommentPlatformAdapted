from django.http import HttpResponse
from django.shortcuts import render_to_response
import xml.etree.ElementTree as xml
import misitio.models.Comentario
import datetime

def registrarComentario(request):
    datosComentario =  request.raw_post_data
    tree = xml.fromstring(datosComentario)
    
    for i in tree.iter(): 
	if i.tag == "texto":
	        texto = i.text
	elif i.tag == "adjunto":
		adjunto = i.text
	elif i.tag == "nickName":
		nickName = i.text
	elif i.tag == "token":
		token = i.text
    now = datetime.datetime.now()
    elComentario = misitio.models.Comentario.Comentario(texto, adjunto, nickName, token, str (now))
    
	
    if elComentario.registrarComentario() == "TRUE":	
	    return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Se ha agregado satisfactoriamente el Comentario el dia: "+elComentario.fecha},mimetype='application/xml')
    else:
	    return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Error al tratar de generar el Comentario el dia: 		    "+elComentario.fecha},mimetype='application/xml')
