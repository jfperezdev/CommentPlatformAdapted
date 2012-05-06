import pycassa
from pycassa.pool import ConnectionPool
from pycassa.columnfamily import ColumnFamily

class Comentario:
	def __init__ (self, texto, adjunto, nickName, token, fecha):
		self.texto = texto
                self.adjunto = adjunto
		self.nickName = nickName
		self.token = token
                self.fecha = fecha

	def registrarComentario (self):
		try:
			    pool = ConnectionPool('baseDeDatos')
		    	    col_fam = pycassa.ColumnFamily(pool, 'Comentario')	
			    col_fam.insert (self.nickName, {'texto': self.texto ,'adjunto': self.adjunto, 'fecha': self.fecha})
		except Exception:
		     return "FALSE"
		else:
		     return "TRUE"
	
