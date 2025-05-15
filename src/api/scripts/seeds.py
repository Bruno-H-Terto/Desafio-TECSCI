import json
from datetime import datetime
from pathlib import Path

from api.models import Metric, Plant, Inverter, table_registry
from config.database import get_session, engine

print('Droped database')
table_registry.metadata.drop_all(bind=engine)
print('Create new database')
table_registry.metadata.create_all(bind=engine)


with get_session() as session:
    plant1 = Plant(plant_name="Usina 1")
    plant2 = Plant(plant_name="Usina 2")
    session.add_all([plant1, plant2])
    session.commit()

    inverters_plant1 = [Inverter(plant_id=plant1.id) for _ in range(4)]
    inverters_plant2 = [Inverter(plant_id=plant2.id) for _ in range(4)]

    session.add_all(inverters_plant1 + inverters_plant2)
    session.commit()
    print('Plants and Inverters registered successfully')


json_path = Path('src/api/sample/metrics.json')
with open(json_path, 'r', encoding='utf-8') as file:
    raw_data = json.load(file)

clean_data = []
for item in raw_data:
    datetime_value = datetime.fromisoformat(item['datetime']['$date'].replace('Z', '+00:00'))
    power_value = item.get('potencia_ativa_watt', 0) or 0
    temp_celsius_value = item.get('temperatura_celsius', 0) or 0

    clean_data.append({
        'datetime': datetime_value,
        'inverter_id': item['inversor_id'],
        'power': power_value,
        'temp_celsius': temp_celsius_value,
    })

with get_session() as session:
    for record in clean_data:
        session.add(Metric(**record))
    session.commit()

print('Metrics registered successfully')
