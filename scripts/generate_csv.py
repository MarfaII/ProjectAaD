#только нужненькое
from datetime import datetime, timedelta
import random
import pandas as pd
import configparser
import os
from uuid import uuid4

#путь для текущей директории и на уровень выше
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)


# pагрузка конфигурации
config = configparser.ConfigParser()
config.read(os.path.join(current_dir,'config.ini'))


# чтение параметров генерации из секции [generator]
MIN_SHOP = int(config['generator']['min_shop'])
MAX_SHOP = int(config['generator']['max_shop']) 


MIN_CASH = int(config['generator']['min_cash'])
MAX_CASH = int(config['generator']['max_cash'])

MIN_ITEMS_IN_CHECK = int(config['generator']['min_items_in_check'])
MAX_ITEMS_IN_CHECK = int(config['generator']['max_items_in_check'])

MIN_CHECKS = int(config['generator']['min_checks'])
MAX_CHECKS = int(config['generator']['max_checks'])

MIN_PRICE = float(config['generator']['min_price'])
MAX_PRICE = float(config['generator']['max_price'])

MAX_DISCOUNT_PERC = float(config['generator']['max_discount_perc'])
DISCOUNT_PROB = float(config['generator']['discount_prob'])

# чтение категорий товаров из секции [Categories]
CATEGORIES = {}
for category in config['Categories']:
    items = config['Categories'][category].split(',')
    CATEGORIES[category] = [item.strip() for item in items]

# генерация строк для одного чека 
def generate_check_lines(num_lines):
    rows = []
    doc_id = str(uuid4())[:8]  # Уникальный ID чека (сокращённый UUID)
    for _ in range(num_lines):
        category = random.choice(list(CATEGORIES.keys()))
        item = random.choice(CATEGORIES[category])
        amount = random.randint(1, 5)
        price = round(random.uniform(MIN_PRICE, MAX_PRICE), 2)
        discount = round(random.uniform(0, price * MAX_DISCOUNT_PERC), 2) if random.random() < DISCOUNT_PROB else 0
        rows.append({
            "doc_id": doc_id,
            "item": item,
            "category": category,
            "amount": amount,
            "price": price,
            "discount": discount
        })
    return rows

# генерация CSV-файлов для всех магазинов
def generate_csv_files(num_shops):
    output_dir = os.path.join(parent_dir, "data")
    os.makedirs(output_dir, exist_ok=True)

    for shop_num in range(1, num_shops + 1):
        num_cashes = random.randint(MIN_CASH, MAX_CASH)
        for cash_num in range(1, num_cashes + 1):
            rows = []
            num_checks = random.randint(MIN_CHECKS, MAX_CHECKS)
            for _ in range(num_checks):
                rows.extend(generate_check_lines(random.randint(MIN_ITEMS_IN_CHECK, MAX_ITEMS_IN_CHECK)))
            df = pd.DataFrame(rows)
            filename = f"{shop_num}_{cash_num}.csv"
            filepath = os.path.join(output_dir, filename)
            df.to_csv(filepath, index=False, encoding='utf-8')
            print(f"✅ Сгенерирован файл: {filepath}")

# 5,4,3,2,1,пуск
print(f"📅 Генерация на дату: {datetime.now().date()}")
num_shops = random.randint(MIN_SHOP, MAX_SHOP)
generate_csv_files(num_shops)
