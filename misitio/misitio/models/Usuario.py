import pycassa
from pycassa.pool import ConnectionPool
from pycassa.columnfamily import ColumnFamily

class Usuario:
	def __init__(self, nickName, password, primerNombre, segundoNombre, primerApellido, segundoApellido, email, fechaNacimiento, paisOrigen, biografia, foto):
		self.nickName = nickName
                self.password = password
		self.primerNombre = primerNombre
                self.segundoNombre = segundoNombre
                self.primerApellido = primerApellido
                self.segundoApellido = segundoApellido
		self.email = email                
		self.fechaNacimiento = fechaNacimiento                
                self.paisOrigen = paisOrigen
                self.biografia = biografia
                self.foto = foto 
	

	def registrarse(self): 
	    try:
		    pool = ConnectionPool('baseDeDatos')
	    	    col_fam = pycassa.ColumnFamily(pool, 'Usuario')	
		    col_fam.insert (self.nickName, {'password': self.password
		    ,'primerNombre': self.primerNombre
		    ,'segundoNombre': self.segundoNombre
		    ,'primerApellido': self.primerApellido
		    ,'segundoApellido': self.segundoApellido
		    ,'email': self.email
		    ,'fechaNacimiento': self.fechaNacimiento
		    ,'paisOrigen': self.paisOrigen
		    ,'biografia': self.biografia
		    ,'foto': self.foto})
            except Exception:
		return "FALSE"
	    else:
		return "TRUE"

	def modificarse(self):
	    
	    try:
		    pool = ConnectionPool('baseDeDatos')
	    	    col_fam = pycassa.ColumnFamily(pool, 'Usuario')	
		    col_fam.insert (self.nickName, {'password': self.password
		    ,'primerNombre': self.primerNombre
		    ,'segundoNombre': self.segundoNombre
		    ,'primerApellido': self.primerApellido
		    ,'segundoApellido': self.segundoApellido
		    ,'email': self.email
		    ,'fechaNacimiento': self.fechaNacimiento
		    ,'paisOrigen': self.paisOrigen
		    ,'biografia': self.biografia
		    ,'foto': self.foto})
            except Exception:
		return "FALSE"
	    else:
		return "TRUE"

 	def validarSesion(self,nickName):
	     try:
	    	    pool = ConnectionPool('baseDeDatos')
	    	    col_fam = pycassa.ColumnFamily(pool, 'Usuario')
		    resultado = col_fam.get(self.nickName,columns=['password'])
		    clave = resultado['password']

		    if(self.nickName == nickName) and (clave == self.password):
			   return "TRUE"
		    else:
		           return "FALSE"
             except Exception: 
		return "FALSE"

