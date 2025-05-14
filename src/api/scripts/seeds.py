import json
from datetime import datetime
from pathlib import Path

from api.models import Metric
from config.database import get_session

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
        metric = Metric(
            datetime=record['datetime'],
            inverter_id=record['inverter_id'],
            power=record['power'],
            temp_celsius=record['temp_celsius'],
        )
        session.add(metric)
    session.commit()

print('File registered successfully')
