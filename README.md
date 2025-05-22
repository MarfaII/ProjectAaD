# Итоговая работа по разделу "Автоматизация и Деплой"
# Курса-симулятора "Аналитик данных"
# Школы Simulative 

Проект предназначен для генерации фейковых данных о продажах, создания таблицы в PostgreSQL и загрузки этих данных в базу. Скрипт может быть запущен ежедневно по расписанию (например, через `cron`).

## Структура проекта

- `generate_csv.py` — генерация CSV-файла с данными о продажах.
- `create_DB.py` — создание базы данных (при первом запуске).
- `schemaDB.sql` — SQL-скрипт с определением таблицы `sales`.
- `from_csv_to_DB.py` — загрузка данных из CSV в БД.
- `daily_run.py` — единая точка запуска: сгенерировать CSV и загрузить в БД.
- `config.ini` — конфигурационный файл с настройками генератора и БД.
- `requirements.txt` — зависимости Python.

## Технологии

- Python 3.11+
- PostgreSQL
- Pandas, NumPy
- `psycopg2` для подключения к БД

## Как развернуть проект

### 1. Установите зависимости
```bash
pip install -r requirements.txt
```

### 2. Измените параметры подключения к базе данных в config.ini
```ini
[DataBase]
HOST=your_host
PORT=5432
DATABASE=your_db
USER=your_user
PASSWORD=your_password
```
### 3. Создайте таблицу в базе - запустите скрипт:

```bash
python create_DB.py
```
Либо вручную выполните SQL из schemaDB.sql в вашей PostgreSQL.

### 4. Проверьте работу проекта
```bash
python daily_run.py
```
Если всё настроено верно — CSV-файл будет сгенерирован и загружен в таблицу sales.

### 5. Настройка по расписанию (cron)
Чтобы запускать скрипт ежедневно, настройте cron:

Откройте редактор задач:

```bash
crontab -e
```
Добавьте строку (пример: запуск в 09:00 каждый день):

```cron
0 9 * * * /usr/bin/python3 /home/username/projects/data-sales-loader/daily_run.py >> /home/username/projects/data-sales-loader/log.txt 2>&1
```
Замените путь на актуальный. Логи будут сохраняться в log.txt.

## Пример данных
CSV содержит строки вида:

```doc_id,item,category,amount,price,discount,shop_num,cash_num,load_date
ABC123,Гель для душа,бытовая химия,2,399.99,0.00,3,1,2025-05-21
```

### Автор работы:
#### Казанцева Марина
e-mail: marfa_II@mail.ru