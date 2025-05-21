
import os
import configparser

#загружаем самомозданный скласс для БД (pgdb.py)
from pgdb import PGDataBase 



#путь для текущей директории и на уровень выше
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)


# pагрузка конфигурации
config = configparser.ConfigParser()
config.read(os.path.join(current_dir,'config.ini'))

# конфигурация подключения 
DATABASE_ = config['DataBase']


#создаем экземпляр класса БД

database = PGDataBase(
    host=DATABASE_['HOST'],   
    port=DATABASE_['PORT'],
    database=DATABASE_['DATABASE'],
    user=DATABASE_['USER'],
    password=DATABASE_['PASSWORD']
)

# Загрузка SQL-скрипта
with open("schemaDB.sql", "r", encoding="utf-8") as f:
    schema_sql = f.read()

# Подключение к БД и выполнение скрипта
try:
    database.post(schema_sql)
    print("✅ Таблица успешно создана в базе PostgreSQL")
except Exception as e:
    print("❌ Ошибка при создании таблицы:", e)
