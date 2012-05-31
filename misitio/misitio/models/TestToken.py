from django.utils import unittest
import Token as GestionToken
import datetime

class TokenTestCase(unittest.TestCase):

    def test_insertarToken(self):
        elToken = GestionToken.Token()
        elToken.nickName = "Cisco"
        ip = "127.0.0.1" 
        elToken.ip = ip
        respuesta = elToken.insertarToken()
        print "-------------------------------------------------------------------"
        print "------------------TEST INSERTAR TOKEN -----------------------------" 
	print "La funcion retorna \n "+respuesta    
        self.assertNotEqual(respuesta,"FALSE")
    
    def test_tieneToken(self):
        elToken = GestionToken.Token()
        elToken.nickName = "Cisco"
        ip = "127.0.0.1" 
        elToken.ip = ip
        respuesta = elToken.tieneToken()
        print "-------------------------------------------------------------------"
        print "------------------TEST TIENE TOKEN --------------------------------" 
	print "La funcion retorna \n "+respuesta    
        self.assertEqual(respuesta,"TRUE")

unittest.main()
    
