from django.http import HttpResponse
from django.shortcuts import render_to_response
import xml.etree.ElementTree as xml
import misitio.models.Token as GestionToken
import datetime
import pycassa
from pycassa.pool import ConnectionPool
from pycassa.columnfamily import ColumnFamily


############################################################
#----------------- Verificar Token-------------------------#
def verificarToken(request):

    datosToken =  request.raw_post_data
    tree = xml.fromstring(datosToken) 
    ip = str(request.META['REMOTE_ADDR']) 

    for i in tree.iter(): 
	if i.tag == "token":
	        nickName = i.text
	
    now = datetime.datetime.now()

    elToken = GestionToken.Token()
    elToken.ip = ip
    elToken.token = token
    
	    
    if elToken.validarToken == "TRUE":	
       return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Correcto"},mimetype='application/xml')
    else:
       return render_to_response('respuestaMensaje.xml', {'mensajeRespuesta': "Incorrecto"},mimetype='application/xml')

