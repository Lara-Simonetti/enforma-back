from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

EjercicioRutina = db.Table("EjercicioRutina",\
    db.Column("rutina_id", db.Integer, db.ForeignKey('rutina.id'), primary_key = True),\
    db.Column("ejercicio_id", db.Integer, db.ForeignKey('ejercicio.id'), primary_key = True))

class Ejercicio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128))
    descripcion = db.Column(db.String(512))
    video = db.Column(db.String(512))
    calorias = db.Column(db.Numeric)
    entrenamientos = db.relationship('EntrenamientoEjercicio')
    rutinas = db.relationship('Rutina', secondary='EjercicioRutina', back_populates="ejercicioRutina")
    duracionRutina = db.Column(db.Numeric, default=0)
    repeticionesRutina = db.Column(db.Numeric, default=0)

class Persona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128))
    apellido = db.Column(db.String(128))
    talla = db.Column(db.Numeric)
    peso = db.Column(db.Numeric)
    edad = db.Column(db.Numeric)
    ingreso = db.Column(db.Date)
    brazo = db.Column(db.Numeric)
    pecho = db.Column(db.Numeric)
    cintura = db.Column(db.Numeric)
    pierna = db.Column(db.Numeric)
    entrenando = db.Column(db.Boolean, default=True)
    razon = db.Column(db.String(512))
    terminado = db.Column(db.Date)
    entrenamientos_ejercicio = db.relationship('EntrenamientoEjercicio', cascade='all, delete, delete-orphan')
    entrenamientos_rutina = db.relationship('EntrenamientoRutina', cascade='all, delete, delete-orphan')
    usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50))
    contrasena = db.Column(db.String(50))
    personas = db.relationship('Persona', cascade='all, delete, delete-orphan')


class EntrenamientoEjercicio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tiempo = db.Column(db.Time)
    repeticiones = db.Column(db.Numeric)
    fecha = db.Column(db.Date)
    ejercicio = db.Column(db.Integer, db.ForeignKey('ejercicio.id'))
    persona = db.Column(db.Integer, db.ForeignKey('persona.id'))


class EntrenamientoRutina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tiempo = db.Column(db.Time)
    fecha = db.Column(db.Date)
    rutina = db.Column(db.Integer, db.ForeignKey('rutina.id'))
    persona = db.Column(db.Integer, db.ForeignKey('persona.id'))


class Rutina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True)
    descripcion = db.Column(db.String(250))
    duracion_minutos = db.Column(db.String(250))
    entrenamientos = db.relationship('EntrenamientoRutina')
    ejercicioRutina = db.relationship('Ejercicio', secondary='EjercicioRutina', back_populates="rutinas")

class EjercicioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Ejercicio
        include_relationships = True
        include_fk = True
        load_instance = True
        
    id = fields.String()
    calorias = fields.String()
    duracionRutina = fields.String()
    repeticionesRutina = fields.String()


class PersonaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Persona
        include_relationships = True
        include_fk = True
        load_instance = True
        
    id = fields.String()
    talla = fields.String()
    peso = fields.String()
    edad = fields.String()
    brazo = fields.String()
    pecho = fields.String()
    cintura = fields.String()
    pierna = fields.String()


class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True
        
    id = fields.String()
        
class RutinaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Rutina
        include_relationships = True
        load_instance = True
        
    id = fields.String()
    nombre = fields.String()
    descripcion = fields.String()
    duracion_minutos = fields.String()
    ejercicioRutina = fields.Nested("EjercicioSchema", many=True)

class ReporteGeneralSchema(Schema):
    persona = fields.Nested(PersonaSchema())
    imc = fields.Float()
    clasificacion_imc = fields.String()

class ReporteDetalladoSchema(Schema):
    fecha = fields.String()
    repeticiones = fields.Float()
    calorias = fields.Float()
    

class EntrenamientoEjercicioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EntrenamientoEjercicio
        include_relationships = True
        include_fk = True
        load_instance = True
    
    id = fields.String()
    repeticiones = fields.String()


class EntrenamientoRutinaShema(SQLAlchemyAutoSchema):
    class Meta:
        model = EntrenamientoRutina
        include_relationships = True
        include_fk = True
        load_instance = True

    id = fields.String()
