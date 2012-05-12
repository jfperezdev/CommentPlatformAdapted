import pycassa
from pycassa.pool import ConnectionPool
from pycassa.columnfamily import ColumnFamily
import smtplib

class Comentario:
	pass

	def registrarComentario (self):
		try:
		    pool = ConnectionPool('baseDeDatos')
		    col_fam = pycassa.ColumnFamily(pool,'Comentario')
		    elId = generarIdComentario()
		    if(elId != "FALSE"):
		    	self.idComentario = elId 
		    	col_fam.insert (self.idComentario, {'nickName': self.nickName,'texto': self.texto ,'adjunto': self.adjunto, 'admiteRespuesta': self.admiteRespuesta, 'fecha': self.fecha, 'token': self.token})
		    else:
			return "FALSE"
		except Exception:
		     return "FALSE"
		else:
		     return "TRUE"
	

	def responderComentario(self):
		try:
			    pool = ConnectionPool('baseDeDatos')
		    	    col_fam = pycassa.ColumnFamily(pool,'Comentario')
		    	    elId = generarIdComentario()
		    	    if(elId != "FALSE"):
		    	       self.idRespuesta = elId 
			    col_fam.insert (self.idRespuesta, {'nickName': self.nickName,'idComentario': self.idComentario,'usuarioRespuesta': 		self.usuarioRespuesta,'texto': self.texto ,'adjunto': self.adjunto, 'fecha': self.fecha, 'token': self.token})
		except Exception:
		     return "FALSE"
		else:
		     return "TRUE"

############################################################
#-------------------- Admite Respuesta --------------------#

	def admitirRespuesta(self,idComentario):

		try:
		
			pool = ConnectionPool('baseDeDatos')
			col_fam = pycassa.ColumnFamily(pool, 'Comentario')
			resultado = col_fam.get(idComentario,columns=['admiteRespuesta']) 
			admiteRespuesta = resultado['admiteRespuesta']
	
			if (admiteRespuesta == "True"):
				return "TRUE"
			else:
				return "FALSE"
		except Exception:
			     return "FALSE"
		else:
			return "TRUE"




##########################################################################
#-------------------- Notificar respuesta comentario --------------------#

	def notificarRespuestaComentario(self,usuarioRespuesta):
		try:

			pool = ConnectionPool('baseDeDatos')
			col_fam = pycassa.ColumnFamily(pool, 'Usuario')
			resultado = col_fam.get(usuarioRespuesta,columns=['email']) 
			emailDestinatario = resultado['email']
		
			De = "equipoafkdesarrollo"
			texto = "La Plataforma de intercambio de mensajes PlataformCommentAdapted le informa que ud ha recibido una respuesta a un 					 comentario\n----------------------------------------------------------------------------------------------------------------\nPara mayor informacion inicie sesion con su cuenta y mantengase siempre comunicado(a) \n\n 								                    Atentamente:\n Equipo de PlataformCommentAdapted"
			
			server = smtplib.SMTP("smtp.gmail.com:587")
			server.starttls()
			server.login("equipoafkdesarrollo", "kristian1234")
			server.sendmail(De, emailDestinatario, texto)
			server.quit()

		except Exception:
			     return "FALSE"
		else:
			return "TRUE"







############################################################
#----------------- registrar me Gusta--------------------#

	def ponerMeGusta(self):
		try:
			pool = ConnectionPool('baseDeDatos')
		    	col_fam = pycassa.ColumnFamily(pool,'Gusto')
		   	resultado = col_fam.get_range(column_start='idComentario', column_finish='nickName')
			for key,columns in resultado:
			       if(columns['nickName'] == nickName and columns['idComentario'] == idComentario):
					return 'FALSE'
			
			if(elId != "FALSE"):
			       elId = generarIdGusta()
		    	       self.idRespuesta = elId 
			       col_fam.insert (self.idRespuesta, {'idComentario': self.idComentario,'nickName': self.nickName})
			       
		except Exception:
		     return "FALSE"
		else:
		     return "TRUE"

############################################################
#----------------- GenerarId Comentario--------------------#

def generarIdComentario():
		vacio = True
		cont = 0
		try:
			pool = ConnectionPool('baseDeDatos')
			col_fam = pycassa.ColumnFamily(pool,'Comentario')
			resultado = col_fam.get_range(column_start='nickName', column_finish='texto')
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

############################################################
#-------------------- Lista  Comentario--------------------#
def listaComentario(nickName):
	pool = ConnectionPool('baseDeDatos')
	col_fam = pycassa.ColumnFamily(pool, 'Comentario')
	resultado = col_fam.get_range(column_start='adjunto', column_finish='token')
	encontrado = False
	listaDeComentarios = []
	for key,columns in resultado:
		if columns['nickName'] == nickName:
			listaDeComentarios.append(columns['nickName']+":"+columns['texto']+":"+columns['token']+":"+columns['adjunto'])
		encontrado = True

	if(encontrado):
		return listaDeComentarios
	else:
	        return "FALSE"





############################################################
#-------------------- Lista  Respuesta --------------------#
	def listaRespuesta(usuarioRespuesta):
	
		pool = ConnectionPool('baseDeDatos')
		col_fam = pycassa.ColumnFamily(pool, 'Comentario')
		resultado = col_fam.get_range(column_start='adjunto', column_finish='usuarioRespuesta')
		encontrado = False
		listaDeComentarios = []
		for key,columns in resultado:
			if len(columns)>5 and columns['usuarioRespuesta'] == usuarioRespuesta:
				listaDeComentarios.append(columns['usuarioRespuesta']+":"+columns['nickName']+":"+columns['texto']+":"+columns['token']+":"+columns['adjunto'])
			encontrado = True

		if(encontrado):
			return listaDeComentarios
		else:
			return "FALSE"




############################################################
#----------------- GenerarId Gusta--------------------#

def generarIdGusta():
		vacio = True
		cont = 0
		try:
			pool = ConnectionPool('baseDeDatos')
			col_fam = pycassa.ColumnFamily(pool,'Gusto')
			resultado = col_fam.get_range(column_start='idComentario', column_finish='nickName')
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






