import json
import hashlib
from unittest import TestCase

from faker import Faker
from faker.generator import random
from modelos import db, Usuario, EntrenamientoRutina, Rutina

from app import app


class TestEntrenamientoTestCase(TestCase):

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
        self.entrenamientos_creados = []
        
    
    def tearDown(self):
        for entrenamiento_creado in self.entrenamientos_creados:
            entrenamientoRutina = EntrenamientoRutina.query.get(entrenamiento_creado.id)
            db.session.delete(entrenamientoRutina)
            db.session.commit()

        for rutina_creada in self.rutinas_creadas:
            rutina = Rutina.query.get(rutina_creada.id)
            db.session.delete(rutina)
            db.session.commit()
            
        usuario_login = Usuario.query.get(self.usuario_id)
        db.session.delete(usuario_login)
        db.session.commit()

    def test_crear_entrenamiento_rutina(self):
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

        #Crear rutina
        endpoint_rutinas = '/rutina'
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        
        resultado_nueva_rutina = self.client.post(endpoint_rutinas,
                                                   data=json.dumps(nueva_rutina),
                                                   headers=headers)
        datos_rutina = json.loads(resultado_nueva_rutina.get_data())
        print(datos_rutina)

        #Crear los datos de la persona
        nombre_nueva_persona = self.data_factory.first_name()
        apellido_nueva_persona = self.data_factory.last_name()
        talla_nueva_persona = random.randint(50,100)
        peso_nueva_persona = random.randint(50,100)
        edad_nueva_persona = random.randint(20,70)
        ingreso_nueva_persona= '2012-02-21'
        terminado_nueva_persona= '2012-02-21'
        brazo_nueva_persona = random.randint(50,100)
        pecho_nueva_persona = random.randint(50,100)
        cintura_nueva_persona = random.randint(50,100)
        pierna_nueva_persona = random.randint(50,100)
        
        #Crear el json con la persona a crear
        nueva_persona = {
            "nombre": nombre_nueva_persona,
            "apellido": apellido_nueva_persona,
            "talla": talla_nueva_persona,
            "peso": peso_nueva_persona,
            "edad": edad_nueva_persona,
            "ingreso": ingreso_nueva_persona,
            "brazo": brazo_nueva_persona,
            "entrenando": True,
            "razon": "",
            "terminado": terminado_nueva_persona,
            "pecho": pecho_nueva_persona,
            "cintura": cintura_nueva_persona,
            "pierna": pierna_nueva_persona
        }

        #Crear persona
        endpoint_personas = '/personas/{}'.format(self.usuario_id)
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        
        resultado_nueva_persona = self.client.post(endpoint_personas,
                                                   data=json.dumps(nueva_persona),
                                                   headers=headers)
        datos_persona = json.loads(resultado_nueva_persona.get_data())

        #Crear los datos del entrenamiento
        tiempo_nuevo_entrenamiento = self.data_factory.time()
        fecha_nuevo_entrenamiento = '2023-05-08'


        #Crear el json con el entrenamiento a crear
        nuevo_entrenamiento = {
            "tiempo": tiempo_nuevo_entrenamiento,
            "fecha": fecha_nuevo_entrenamiento,
            "rutina": datos_rutina['id'],
        }

        #Definir endpoint, encabezados y hacer el llamado
        endpoint_entrenamientos = '/entrenamientos/rutinas/{}'.format(datos_persona['id'])
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        
        resultado_nuevo_entrenamiento = self.client.post(endpoint_entrenamientos,
                                                   data=json.dumps(nuevo_entrenamiento),
                                                   headers=headers)
                                                                    
        #Obtener los datos de respuesta y dejarlos un objeto json y en el objeto a comparar
        datos_respuesta = json.loads(resultado_nuevo_entrenamiento.get_data())
        entrenamiento = EntrenamientoRutina.query.get(datos_respuesta['id'])
        self.entrenamientos_creados.append(entrenamiento)
                                                   
        #Verificar que el llamado fue exitoso y que el objeto recibido tiene los datos iguales a los creados
        self.assertEqual(resultado_nuevo_entrenamiento.status_code, 200)
        self.assertEqual(tiempo_nuevo_entrenamiento, entrenamiento.tiempo.strftime("%H:%M:%S"))
        self.assertEqual(fecha_nuevo_entrenamiento, entrenamiento.fecha.strftime("%Y-%m-%d"))
        self.assertEqual(int(datos_rutina['id']), entrenamiento.rutina)