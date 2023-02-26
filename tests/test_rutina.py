import json
import hashlib
from unittest import TestCase

from faker import Faker
from faker.generator import random
from modelos import db, Usuario, Rutina

from app import app


class TestRutinaTestCase(TestCase):

    def setUp(self):
        self.data_factory = Faker()
        self.client = app.test_client()
        
        nombre_usuario = 'test_' + self.data_factory.name()
        contrasena = 'T1$' + self.data_factory.word()
        contrasena_encriptada = hashlib.md5(contrasena.encode('utf-8')).hexdigest()
        
        # Se crea el usuario para identificarse en la aplicación
        usuario_nuevo = Usuario(usuario=nombre_usuario, contrasena=contrasena_encriptada)
        db.session.add(usuario_nuevo)
        db.session.commit()

        
        usuario_login = {
            "usuario": nombre_usuario,
            "contrasena": contrasena
        }

        solicitud_login = self.client.post("/login",
                                                data=json.dumps(usuario_login),
                                                headers={'Content-Type': 'application/json'})

        respuesta_login = json.loads(solicitud_login.get_data())

        self.token = respuesta_login["token"]
        self.usuario_id = respuesta_login["id"]
        
        self.rutinas_creadas = []
        
    
    def tearDown(self):
        for rutina_creada in self.rutinas_creadas:
            rutina = Rutina.query.get(rutina_creada.id)
            db.session.delete(rutina)
            db.session.commit()
            
        usuario_login = Usuario.query.get(self.usuario_id)
        db.session.delete(usuario_login)
        db.session.commit()

    def test_crear_rutina(self):
        #Crear los datos de la rutina
        nombre_nueva_rutina = self.data_factory.sentence()
        descripcion_nueva_rutina = self.data_factory.sentence()
        minutos_nueva_rutina = random.randint(10,90)
        
        #Crear el json con la rutina a crear
        nueva_rutina = {
            "nombre": nombre_nueva_rutina,
            "descripcion": descripcion_nueva_rutina,
            "duracion_minutos": minutos_nueva_rutina,
        }
        
        #Definir endpoint, encabezados y hacer el llamado
        endpoint_rutinas = "/rutina"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        
        resultado_nueva_rutina = self.client.post(endpoint_rutinas,
                                                   data=json.dumps(nueva_rutina),
                                                   headers=headers)
                 
                                                   
        #Obtener los datos de respuesta y dejarlos un objeto json y en el objeto a comparar
        datos_respuesta = json.loads(resultado_nueva_rutina.get_data())
        rutina = Rutina.query.get(datos_respuesta['id'])
        self.rutinas_creadas.append(rutina)
                                                   
        #Verificar que el llamado fue exitoso y que el objeto recibido tiene los datos iguales a los creados
        self.assertEqual(resultado_nueva_rutina.status_code, 200)
        self.assertEqual(datos_respuesta['nombre'], rutina.nombre)
        self.assertEqual(datos_respuesta['descripcion'], rutina.descripcion)
        self.assertEqual(float(datos_respuesta['duracion_minutos']), float(rutina.duracion_minutos))
        self.assertIsNotNone(datos_respuesta['id'])
