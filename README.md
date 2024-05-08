# NBA Managment Database

В этом проекте представленна база данных предназначенная для управляющих баскетбольной лигой

База данных хранит информацию и историю о взаимодействии игроков и команд, тренеров и команд, а также игр между командами

---
### Структура проекта:
```
├── data
|   ├── coaches.csv
|   └── teams.csv
|
├── docs
|   ├── consept-model.png
|   ├── logic-model.png
|   └── physical-model.md
|
├── src
|   ├── analytics_outputs
|   ├── sql_scripts
|   |   ├── create_tables.sql
|   |   ├── drop_all.sql
|   |   ├── inserts.sql
|   |   └── queries.sql
|   |
|   ├── analytics.ipynb
|   ├── config.py
|   ├── insert.py
|   └── pg_client.py
|   
├── tests
|   ├── test_queries.py
|   └── test_table_creation.
|
├── pytest.ini
└── README.md
```

### Создать базу локально:
Для создания базы локально измените данные в файле config.py.
Затем запустите последоваьельно create_tables.sql, insert.py, inserts.sql

### Запустить тесты запросов и создания таблиц:
```console
pytest -v
```

### Посмотреть примеры аналитики данных из базы:
Это можно сделать в analytics.ipynb (выводы ячеек в папке analytics_outputs)
