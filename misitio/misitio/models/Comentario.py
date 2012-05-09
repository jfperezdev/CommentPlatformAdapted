import pycassa
from pycassa.pool import ConnectionPool
from pycassa.columnfamily import ColumnFamily

class Comentario:
	pass

	def registrarComentario (self):
		try:
		    pool = ConnectionPool('baseDeDatos')
		    col_fam = pycassa.ColumnFamily(pool,'Comentario')
		    elId = generarIdComentario()
		    if(elId != "FALSE"):
		    	self.idComentario = elId 
		    	col_fam.insert (self.idComentario, {'nickName': self.nickName,'texto': self.texto ,'adjunto': self.adjunto, 'fecha': self.fecha, 'token': self.token})
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
#----------------- GenerarId Comentario--------------------#

def generarIdComentario():
		vacio = True
		try:
			pool = ConnectionPool('baseDeDatos')
			col_fam = pycassa.ColumnFamily(pool,'Comentario')
			resultado = col_fam.get_range(column_start='nickName', column_finish='texto')
			arreglo = []

			for key,columns in resultado:
				arreglo.append(key)
				vacio = False

			listaIdComentario = sorted(arreglo,reverse=True)

		except Exception:
		     return "FALSE"
		else:
		     if vacio == True:
			return '1'
		     else:
		        nuevoId = unicode(int(listaIdComentario[0]) + 1)
		        return nuevoId
	
