#«Продуктовый помощник»
Cайт, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

#Запуск проекта на сервере
Образы проекта собраны для запуска на linux сервере с архитектурой процессора ARM64 (AArch64)

Для запуска сайта на сервере нужно:

1. Создать файл ```.env``` и задать следующие переменные окружения:
  + ```DB_ENGINE=<django.db.backends.postgresql>```
  + ```DB_NAME=<Имя БД>```
  + ```POSTGRES_USER=<Пользователь БД>```
  + ```POSTGRES_PASSWORD=<Пароль пользователя БД>```
  + ```DB_HOST=<db>```
  + ```DB_PORT=<5432>```
  + ```SECRET_KEY=<секетный ключ Django>```
2. Из папки infra cкопировать файлы на сервер:
  + ```docker-compose.yml```
  + ```nginx.conf```
2. При необходимости, установить docker, последовательно выполняя команды:
  + ```sudo apt install curl```
  + ```curl -fsSL https://get.docker.com -o get-docker.sh```
  + ```sh get-docker.sh```
3. Выполнить команду
  + ```sudo docker-compose up -d```
4. При первом запуске, посл старта контейнеров выполнить команды:
  + ```sudo docker-compose exec -T backend python3 manage.py migrate --noinput```

# Запуск проекта на локальном ПК
ПК с архитектурой x86
1. Клонировать репозиторий
2. Находясь в папке infra выполнить команду:
  + ```docker-compose up -f docker-compose.dev_gunicorn.yml```

После выполнения этих команд, запустится сборка образов. По окончании сборки запустятся контейнеры. В контейнере backend запустится gunicorn, отслеживающий изменения в коде проекта. При изменении кода gunicorn самостоятельно перезапустится.

# Отладка в PyCharm
При настройке отладки в PyCharm, в качестве следует использовать remote interpreter, работающий с docker-compose.dev.yml

Для запуска и отладки Django Server и Django Tests необходимо установить переменные среды:

+ ```PYTHONUNBUFFERED=1```
+ ```DJANGO_SETTINGS_MODULE=backend.settings_dev```

При отладке в PyCharm используется встроенный сервер Django.

#Работающий проект
Проект доступен по адресу http://foodgram-aybor.tk/ или по IP: http://140.238.175.119/

Администратор:
+ email: admin@admin.ru
+ username: admin
+ password: qwedcxzas


[![Django-app workflow](https://github.com/aybor/foodgram-project-react/actions/workflows/foodgram_project.yml/badge.svg)](https://github.com/aybor/foodgram-project-react/actions/workflows/foodgram_project.yml)