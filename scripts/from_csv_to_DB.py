import pandas as pd
import os
import configparser
import re
import glob
from datetime import datetime
#загружаем самомозданный скласс для БД (pgdb.py)
from pgdb import PGDataBase 


#путь для текущей директории
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)

#работаем с config
config = configparser.ConfigParser()
config.read(os.path.join(current_dir,'config.ini'))
DATABASE_ = config['DataBase']

#собираем данные из data для загузки в БД


# Путь к папке с файлами
DATA_DIR = os.path.join(parent_dir, "data")

# Шаблон названия файла — 12_3.csv, 1_1.csv и т.д.
FILENAME_PATTERN = re.compile(r'^(\d+)_(\d+)\.csv$')

# Ищем все .csv файлы в папке
csv_files = glob.glob(os.path.join(DATA_DIR, "*.csv"))

# Подходящие по имени
valid_files = [f for f in csv_files if FILENAME_PATTERN.match(os.path.basename(f))]

# Список всех подготовленных DataFrame'ов
dataframes = []

for filepath in valid_files:
    filename = os.path.basename(filepath)
    match = FILENAME_PATTERN.match(filename)
    shop_num = int(match.group(1))
    cash_num = int(match.group(2))

    df = pd.read_csv(filepath)

    # Добавляем дополнительные поля
    df["shop_num"] = shop_num
    df["cash_num"] = cash_num
    df["load_date"] = datetime.today().date()

    dataframes.append(df)
    print(f"✅ Подготовлен файл: {filename}")
    
    # После успешной обработки — переместим файл в архив
    archive_dir = os.path.join(parent_dir, "archive")
    os.makedirs(archive_dir, exist_ok=True)

    archived_path = os.path.join(archive_dir, filename)
    os.replace(filepath, archived_path)
    print(f"📁 Перемещён в архив: {archived_path}")


# Объединяем
if dataframes:
    all_data = pd.concat(dataframes, ignore_index=True)
    print(f"📦 Всего строк для загрузки: {len(all_data)}")
else:
    all_data = pd.DataFrame().reset_index()
    print("⚠️ Нет подходящих файлов для обработки")


#создаем экземпляр класса базы данных
database = PGDataBase(
    host=DATABASE_['HOST'],   
    port=DATABASE_['PORT'],
    database=DATABASE_['DATABASE'],
   user=DATABASE_['USER'],
   password=DATABASE_['PASSWORD']
)

#складываем в БД данные из таблички
for i, row in all_data.iterrows():
    query = """
        INSERT INTO sales (
            doc_id, item, category, amount, price, discount, shop_num, cash_num, load_date
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        row['doc_id'],
        row['item'],
        row['category'],
        int(row['amount']),
        float(row['price']),
        float(row['discount']),
        int(row['shop_num']),
        int(row['cash_num']),
        row['load_date']
    )
    database.post(query, values)
    