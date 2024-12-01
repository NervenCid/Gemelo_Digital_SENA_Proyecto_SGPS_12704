#Importamos SQLAlchemy
from sqlalchemy import Column, String, ForeignKey, DECIMAL, TIMESTAMP, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base 

#Importamos uuid
import uuid

# Define a SQLAlchemy model 
Base = declarative_base() 

'''
class User(Base):
    __tablename__ = "User"

    UserID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    Name = Column(String(100), nullable=False)
    Email = Column(String(255), unique=True, nullable=False)
    Password = Column(String(255), nullable=False)
    Role = Column(String(50), nullable=False)

    gateways = relationship("Gateway", back_populates="user")
'''

#Modelo del 'Gateway'    
class Gateway(Base):
    __tablename__ = "Gateway"

    gateway_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    #UserID = Column(UUID(as_uuid=True), ForeignKey("User.UserID"))
    name = Column(String(255), nullable=False)
    imei = Column(String(255), unique=True, nullable=False)
    serial_number = Column(String(255), unique=True, nullable=False)

    #user = relationship("User", back_populates="Gateway")
    em300_sensor = relationship("Em300Sensor", back_populates="gateway")
    em500_sensor = relationship("Em500Sensor", back_populates="gateway")
    weather_station = relationship("WeatherStation", back_populates="gateway")
    sph01lb_sensor = relationship("SPH01LBSensor", back_populates="gateway")

#Modelo del sensor 'Em300'
class Em300Sensor(Base):
    __tablename__ = 'Em300Sensor'
    
    sensor_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    gateway_id  = Column(UUID(as_uuid=True), ForeignKey('Gateway.gateway_id', ondelete='CASCADE'))
    topic = Column(String(255), unique=True, nullable=False)
    model = Column(String(255), nullable=False)
    dev_eui = Column(String(255), nullable=False)
    
    gateway = relationship("Gateway", back_populates="em300_sensor")
    em300_measure = relationship("Em300Measure", back_populates="em300_sensor")
    
#Modelo para todos los sensores 'Em500'
class Em500Sensor(Base):
    __tablename__ = 'Em500Sensor'
    sensor_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    gateway_id = Column(UUID(as_uuid=True), ForeignKey('Gateway.gateway_id', ondelete='CASCADE'))
    topic = Column(String(255), unique=True, nullable=False)
    model = Column(String(255), nullable=False)
    dev_eui = Column(String(255), nullable=False)

    gateway = relationship("Gateway", back_populates="em500_sensor")
    em500_measure = relationship("Em500Measure", back_populates="em500_sensor")

#Modelo para la estacion metereologica
class WeatherStation(Base):
    __tablename__ = 'WeatherStation'
    sensor_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    gateway_id = Column(UUID(as_uuid=True), ForeignKey('Gateway.gateway_id', ondelete='CASCADE'))
    topic = Column(String(255), unique=True, nullable=False)
    model = Column(String(255), nullable=False)
    dev_eui = Column(String(255), nullable=False)

    gateway = relationship("Gateway", back_populates="weather_station")
    weather_station_measure = relationship("WeatherStationMeasure", back_populates="weather_station")

#Modelo para el sensor de PH
class SPH01LBSensor(Base):
    __tablename__ = 'SPH01LBSensor'
    sensor_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    gateway_id = Column(UUID(as_uuid=True), ForeignKey('Gateway.gateway_id', ondelete='CASCADE'))
    topic = Column(String(255), unique=True, nullable=False)
    model = Column(String(255), nullable=False)
    dev_eui = Column(String(255), nullable=False)

    gateway = relationship("Gateway", back_populates="sph01lb_sensor")
    sph01lb_measure = relationship("SPH01LBMeasure", back_populates="sph01lb_sensor")

#Modelo para las medidas del sensor 'Em300'
class Em300Measure(Base):
    __tablename__ = 'Em300Measure'
    measure_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sensor_id = Column(UUID(as_uuid=True), ForeignKey('Em300Sensor.sensor_id', ondelete='CASCADE'))
    timestamp = Column(TIMESTAMP, nullable=False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)

    em300_sensor = relationship("Em300Sensor", back_populates="em300_measure")

#Modelo para las medidas del sensor 'Em500'
class Em500Measure(Base):
    __tablename__ = 'Em500Measure'
    measure_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sensor_id = Column(UUID(as_uuid=True), ForeignKey('Em500Sensor.sensor_id', ondelete='CASCADE'))
    timestamp = Column(TIMESTAMP, nullable=False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    pressure = Column(Float)
    co2 = Column(Float)
    illumination = Column(Float)
    conductivity = Column(Float)
    soil_moisture = Column(Float)

    em500_sensor = relationship("Em500Sensor", back_populates="em500_measure")

#Modelo para las medidas de la estacion metereologica
class WeatherStationMeasure(Base):
    __tablename__ = 'WeatherStationMeasure'
    measure_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sensor_id = Column(UUID(as_uuid=True), ForeignKey('WeatherStation.sensor_id', ondelete='CASCADE'))
    timestamp = Column(TIMESTAMP, nullable=False)
    battery = Column(Float)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    wind_direction = Column(Float)
    pressure = Column(Float)
    wind_speed = Column(Float)

    weather_station = relationship("WeatherStation", back_populates="weather_station_measure")

#Modelo para las medidas de los sensores de PH
class SPH01LBMeasure(Base):
    __tablename__ = 'SPH01LBMeasure'
    measure_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sensor_id = Column(UUID(as_uuid=True), ForeignKey('SPH01LBSensor.sensor_id', ondelete='CASCADE'))
    timestamp = Column(TIMESTAMP, nullable=False)
    temperature = Column(Float, nullable=False)
    ph = Column(Float, nullable=False)

    sph01lb_sensor = relationship("SPH01LBSensor", back_populates="sph01lb_measure")

