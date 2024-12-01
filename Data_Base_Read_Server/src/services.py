
#Importamos la sesion de la base de datos
from sqlalchemy.orm import Session
from sqlalchemy import func

#Obtenemos la ultima medida de cada dispositivo
def get_last_measurements_for_each_topic(db: Session, sensor_model, measure_model):
    
    #Ejecutamos el Query
    subquery = db.query(
        measure_model.sensor_id,
        func.max(measure_model.timestamp).label("last_timestamp")
    ).group_by(measure_model.sensor_id).subquery()

    query = db.query(
        sensor_model.topic,
        measure_model
    ).join(measure_model, sensor_model.sensor_id == measure_model.sensor_id).join(
        subquery,
        (measure_model.sensor_id == subquery.c.sensor_id) &
        (measure_model.timestamp == subquery.c.last_timestamp)
    )

    results= query.all()

    # Convertimos los resultados en una lista de diccionarios
    result_dicts = [
        {
            "topic": result[0],  # El primer elemento es el topic
            **{c.name: getattr(result[1], c.name) for c in measure_model.__table__.columns}  # Medida como diccionario
        }
        for result in results
    ]

    return result_dicts