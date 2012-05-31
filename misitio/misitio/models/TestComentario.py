from django.utils import unittest
import Comentario as GestionComentario
import datetime

class ComentarioTestCase(unittest.TestCase):

    def test_registrarComentario(self):
        etiquetas = "Test,Unitario"
        elComentario = GestionComentario.Comentario()        
        now = datetime.datetime.now()
        elComentario.nickName = "Cisco"
        elComentario.texto = "Comentario en plena prueba unitaria"
        elComentario.token = "23"
        elComentario.admiteRespuesta = "True"
        elComentario.fecha = str (now)  
        self.assertNotEqual(elComentario.registrarComentario(etiquetas),"FALSE")

    def test_segundo(self):
        now = datetime.datetime.now()
        elComentario = GestionComentario.Comentario()                

        elComentario.nickName = "Armen"
        elComentario.idComentario = "1"
        elComentario.usuarioRespuesta = "Cisco"
        elComentario.texto = "Respuesta a Comentario en plena prueba unitaria"
        elComentario.admiteRespuesta = "True"
        elComentario.fecha = str(now)
        elComentario.token = "24"
        self.assertEqual(elComentario.responderComentario(),"TRUE")
					
unittest.main()
