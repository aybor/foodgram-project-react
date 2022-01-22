"""
    Скрипт для импорта ингредиентов из ingredients.csv в БД DJango
    Для запуска скрипта нужно выполнить команды:
                                1) manage.py shell
                                2) exec(open('import_ingredients_csv.py').read())
"""

import csv

from tqdm import tqdm

from api.models import Ingredient

CSV_PATH = './ingredients.csv'

countSuccess = 0
Ingredient.objects.all().delete()

with open(CSV_PATH, newline='') as csv_file:
    spamreader = csv.reader(csv_file, delimiter=',', quotechar=',')
    print('Loading...')
    for row in tqdm(spamreader):
        Ingredient.objects.create(pk=countSuccess, name=row[0], measurement_unit=row[1])
        countSuccess += 1
    print(f'{countSuccess} записей успешно создано')
