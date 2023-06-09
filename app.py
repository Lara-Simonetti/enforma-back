from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api

from modelos import db
from vistas import \
    VistaSignIn, VistaLogIn, \
    VistaPersona, VistaPersonas, \
	VistaEjercicio, VistaEjercicios, \
	VistaEntrenamientoEjercicio, VistaEntrenamientoEjercicios, \
    VistaEntrenamientoRutina, VistaEntrenamientoRutinas, \
    VistaReporte, VistaRutinas, VistaRutina

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbapp.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)
api.add_resource(VistaSignIn, '/signin')
api.add_resource(VistaLogIn, '/login')
api.add_resource(VistaPersonas, '/personas/<int:id_usuario>')
api.add_resource(VistaPersona, '/persona/<int:id_persona>')
api.add_resource(VistaEjercicios, '/ejercicios')
api.add_resource(VistaEjercicio, '/ejercicio/<int:id_ejercicio>')
api.add_resource(VistaEntrenamientoEjercicios, '/entrenamientos/ejercicios/<int:id_persona>')
api.add_resource(VistaEntrenamientoEjercicio, '/entrenamiento/ejercicios/<int:id_entrenamiento>')
api.add_resource(VistaEntrenamientoRutinas, '/entrenamientos/rutinas/<int:id_persona>')
api.add_resource(VistaEntrenamientoRutina, '/entrenamiento/rutinas/<int:id_entrenamiento>')
api.add_resource(VistaReporte, '/persona/<int:id_persona>/reporte')
api.add_resource(VistaRutinas, '/rutina')
api.add_resource(VistaRutina, '/rutina/<int:id_rutina>')

jwt = JWTManager(app)
