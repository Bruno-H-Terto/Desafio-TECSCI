# Desafio Backend

Está é uma aplicação desenvolvida por Bruno Herculano, realizada para a segunda etapa do processo seletivo TECSCI.

## Tecnologias

- Python (>=3.13, <4.0)

- FastAPI (>=0.115.12, <0.116.0)

- Uvicorn (>=0.34.2, <0.35.0)

- Pydantic-Settings (>=2.9.1, <3.0.0)

- Alembic (>=1.15.2, <2.0.0)

- psycopg2-binary (>=2.9.10, <3.0.0)

- Ruff (0.11.9)

- Pytest (8.3.5) + pytest-cov (6.1.1)

- Taskipy (1.14.1)

- Factory Boy (3.3.3)

- Docker

## Dependacias

Para seu correto funcionamento é necessário ter o **Docker** instaldo localmente.

### Aliases (opcional)
De forma opcional, é disponibilizado um script com abreviações dos comando de terminal. Caso seja de interesse, basta carregar o arquivo para a liberações dos atalhos com o seguinte comando:

```sh
$ source aliases.sh
```

---
## Execução
Execute o seguinte comando para iniciar a aplicação:

```sh
$ docker compose build
$ docker compose up -d
```

Com o aliases:
```sh
$ dcb
$ dcu
```

### Testes e lint

Para a execução dos testes execute:

```sh
$ docker compose exec app task test
```

Com o aliases:
```sh
$ dce task test
```

O comando acima irá executar o lint (Ruff)
e os testes (Pytest)

### Seeds (método para popular o banco de dados com os dados do arquivo metrics.json)

Execute:

```sh
$ docker compose exec app python src/scripts/seeds.py
```

Com o aliases:
```sh
$ dce task python src/scripts/seeds.py
```


Este comando realiza:
- A criação de **duas Usina**;
- A criação de **8 inversores** com as associções de dos ID's de **1 a 4** pertencendo a Usina 1 e de **5 a 8** a Usina 2;
- Popula o Banco de dados com as informações presentes e metrics.json (src/app/sample/metrics.json)

---

## EndPoints

ℹ️
**A documentação interativa se encontra disponível através da rota /docs e /redoc**

### Usinas (/plants/)

#### Criar Usina  
POST /plants/  
- Descrição: Cria uma nova usina.  
- Request Body:  
  {
    "plant_name": "nome da usina"
  }  
- Resposta:  
  - 201 Created com a usina criada.  
  - 422 Unprocessable Entity em caso de erro de validação.

---

#### Listar Usinas  
GET /plants/  
- Query Parameters:  
  - limit (inteiro, opcional, padrão 5) — número máximo de usinas retornadas.  
  - offset (inteiro, opcional, padrão 0) — deslocamento para paginação.  
- Resposta:  
  - 200 OK com lista de usinas.  
  - 422 Unprocessable Entity em caso de erro.

---

#### Obter Usina específica  
GET /plants/{plant_id}  
- Path Parameter:  
  - plant_id (inteiro) — ID da usina.  
- Resposta:  
  - 200 OK com dados da usina.  
  - 422 Unprocessable Entity em caso de erro.

---

#### Atualizar Usina  
PUT /plants/{plant_id}  
- Path Parameter:  
  - plant_id (inteiro) — ID da usina.  
- Request Body:  
  {
    "plant_name": "novo nome da usina"
  }  
- Resposta:  
  - 200 OK com usina atualizada.  
  - 422 Unprocessable Entity em caso de erro.

---

#### Deletar Usina  
DELETE /plants/{plant_id}  
- Path Parameter:  
  - plant_id (inteiro) — ID da usina.  
- Resposta:  
  - 200 OK confirmando exclusão.  
  - 422 Unprocessable Entity em caso de erro.

---

### Inversores (/inverters/)

#### Criar Inversor  
POST /inverters/  
- Request Body:  
  {
    "plant_id": id_da_usina
  }  
- Resposta:  
  - 201 Created com o inversor criado.  
  - 422 Unprocessable Entity em caso de erro.

---

#### Listar Inversores  
GET /inverters/  
- Query Parameters:  
  - limit (inteiro, opcional, padrão 5) — número máximo de inversores retornados.  
  - offset (inteiro, opcional, padrão 0) — deslocamento para paginação.  
  - plant_id (inteiro, opcional) — filtrar inversores por usina.  
- Resposta:  
  - 200 OK com lista de inversores.  
  - 422 Unprocessable Entity em caso de erro.

---

#### Obter Inversor específico  
GET /inverters/{inverter_id}  
- Path Parameter:  
  - inverter_id (inteiro) — ID do inversor.  
- Resposta:  
  - 200 OK com dados do inversor.  
  - 422 Unprocessable Entity em caso de erro.

---

#### Atualizar Inversor  
PUT /inverters/{inverter_id}  
- Path Parameter:  
  - inverter_id (inteiro) — ID do inversor.  
- Request Body:  
  {
    "plant_id": id_da_usina
  }  
- Resposta:  
  - 200 OK com inversor atualizado.  
  - 422 Unprocessable Entity em caso de erro.

---

#### Deletar Inversor  
DELETE /inverters/{inverter_id}  
- Path Parameter:  
  - inverter_id (inteiro) — ID do inversor.  
- Resposta:  
  - 200 OK confirmando exclusão.  
  - 422 Unprocessable Entity em caso de erro.

---

### Métricas

#### Obter Potência Máxima de um Inversor  
GET /metrics/max_power/{inverter_id}  
- Path Parameter:  
  - inverter_id (inteiro) — ID do inversor.  
- Query Parameters:  
  - start_date (string, formato date-time) — data inicial do intervalo.  
  - end_date (string, formato date-time) — data final do intervalo.  
- Resposta:  
  - 200 OK com lista das potências máximas.  
  - 422 Unprocessable Entity em caso de erro.

---

#### Obter Temperatura Média de um Inversor  
GET /metrics/average_temp/{inverter_id}  
- Path Parameter:  
  - inverter_id (inteiro) — ID do inversor.  
- Query Parameters:  
  - start_date (string, formato date-time) — data inicial do intervalo.  
  - end_date (string, formato date-time) — data final do intervalo.  
- Resposta:  
  - 200 OK com lista das temperaturas médias.  
  - 422 Unprocessable Entity em caso de erro.

---

#### Obter Potência Total por Usina  
GET /metrics/power_by_plant/{plant_id}  
- Path Parameter:  
  - plant_id (inteiro) — ID da usina.  
- Query Parameters:  
  - start_date (string, formato date-time) — data inicial do intervalo.  
  - end_date (string, formato date-time) — data final do intervalo.  
- Resposta:  
  - 200 OK com potência total gerada pela usina.  
  - 422 Unprocessable Entity em caso de erro.

---

#### Obter Potência Total por Inversor  
GET /metrics/power_by_inverter/{inverter_id}  
- Path Parameter:  
  - inverter_id (inteiro) — ID do inversor.  
- Query Parameters:  
  - start_date (string, formato date-time) — data inicial do intervalo.  
  - end_date (string, formato date-time) — data final do intervalo.  
- Resposta:  
  - 200 OK com potência total gerada pelo inversor.  
  - 422 Unprocessable Entity em caso de erro.

---

#### Raiz da API

GET /  
- Resposta:  
  - 200 OK com resposta padrão.

---
