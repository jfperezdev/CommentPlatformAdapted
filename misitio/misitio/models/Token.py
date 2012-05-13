import pycassa
import datetime
import time
from pycassa.pool import ConnectionPool
from pycassa.columnfamily import ColumnFamily

class Token:
	pass

	def validarToken(self):
	     try:
		    now = datetime.datetime.now()
	    	    pool = ConnectionPool('baseDeDatos')
	    	    col_fam = pycassa.ColumnFamily(pool, 'Token')
		    resultado = col_fam.get(self.token,columns=['idToken','ip','fecha','nickName'])
                    clave = resultado['idToken']
                    ip = resultado['ip']
		    nowToken = resultado['fecha']
		    nickName = resultado['nickName']

		    if (ip==self.ip) and(clave == self.token) and (nickName == self.nickName):
			   nowToken2 = resultado['fecha'].split(".")
		    	   nowToken =datetime.datetime(*time.strptime(nowToken2[0],'%Y-%m-%d %H:%M:%S')[0:6])
		    	   diferenciaToken = now - nowToken
			   horas = str(diferenciaToken).split(":")
			   minutos = int(horas[1])
			   if (horas[0]=="0") and (minutos<=4):
			   	return "TRUE"
			   else:
		           	return "Error"
		    else:
		           return "FALSE"
             except Exception:
		return "FALSE"
	     else:
		return "TRUE"





