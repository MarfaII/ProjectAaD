import datetime
import subprocess
import os
import sys

current_dir = os.path.dirname(__file__)


# Проверка: воскресенье?
if datetime.datetime.today().weekday() == 6:
    print("⛔ Сегодня воскресенье — скрипт не запускается")
else:
    print("✅ Запуск: генерация и загрузка данных")

    # Запускаем генерацию файлов
    subprocess.run([sys.executable, os.path.join(current_dir, "generate_csv.py")], check=True)

    # Загружаем в базу
    subprocess.run([sys.executable, os.path.join(current_dir,"from_csv_to_DB.py")], check=True)

    print("🎉 Всё выполнено успешно!")
