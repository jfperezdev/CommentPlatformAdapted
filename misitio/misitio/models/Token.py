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
		    resultado = col_fam.get(self.token,columns=['idToken','ip','fecha'])
                    clave = resultado['idToken']
                    ip = resultado['ip']
		    nowToken = resultado['fecha']
		    
		    #f=open("hola.txt","w")
		    #f.write(str(diferenciaToken))
		    #f.close()

		    if (ip==self.ip) and(clave == self.token):
			   nowToken2 = resultado['fecha'].split(".")
		    	   nowToken =datetime.datetime(*time.strptime(nowToken2[0],'%Y-%m-%d %H:%M:%S')[0:6])
		    	   diferenciaToken = now - nowToken
			   horas = str(diferenciaToken).split(":")
			   minutos = int(horas[1])
			   if (horas[0]=="0") and (minutos<=4):
			   	return "TRUE"
			   else:
		           	return "FALSE"
		    else:
		           return "FALSE"
             except Exception:
		return "FALSE"
	     else:
		return "TRUE"



def validarUsuarioIp(self):
	     try:
		    now = datetime.datetime.now()
	    	    pool = ConnectionPool('baseDeDatos')
	    	    col_fam = pycassa.ColumnFamily(pool, 'Token')
		    resultado = col_fam.get(self.nickName,columns=['idToken','ip','fecha'])

		    resultado = col_fam.get_range(column_start='accion', column_finish='nickName')
		    arreglo = []

		    for key,columns in resultado:
			 
                    	nickName = columns['nickName']
                    	ip = columns ['ip']
		        nowToken = datetime.datetime.now()
		    
		    #f=open("hola.txt","w")
		    #f.write(str(diferenciaToken))
		    #f.close()

		    	if (nickName==self.nickName) and(ip == self.ip):
				   nowToken2 = resultado['fecha'].split(".")
			    	   nowToken =datetime.datetime(*time.strptime(nowToken2[0],'%Y-%m-%d %H:%M:%S')[0:6])
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
