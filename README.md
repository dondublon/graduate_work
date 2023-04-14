# 🥇 Дипломная работа. Профили пользователей

Адрес расположения https://github.com/dondublon/graduate_work .
Предыдущий code review с нашими ответами здесь: https://github.com/dondublon/graduate_work/issues/53d

## 🔀 1. Схемы
- Схемы взаимодействия основных сервисов описаны в формате C4 - level2 и level3. Названия компонентов соответствуют названиям в docker-compose.yml. Со схемами можно ознакомиться в папке ./schemes. 


## ☑️ 2.Загрузка фильмов в БД
1. Запустить все контейнеры.
2. Выполнить миграции для admin_panel
- `docker exec -ti admin_panel_async_api python manage.py migrate`
- `docker exec -ti auth flask db upgrade`
3. Запустить локально файл "/sqlite_to_postgres/load_data.py"

## 🔐 3.Сервис авторизации с системой ролей (Auth)
Для просмотра документации перейдите по `http://0.0.0.0:5001/api/v1/user/`

Коллекция с основными ручками лежит в папке ./auth/auth.postman_collection.json

### Создать суперпользователя

Для этого необходимо перейти в `auth` и ввести команду.
```commandline
flask create-superuser <email>
```
После чего вам предложат ввести пароль, подтвердить его. Итоговый вывод в консоли может выглядеть вот так:
```commandline
(venv) developer@MacBook-Pro auth % flask --app app create-superuser ADMIN@email.com
Enter password: ADMIN
Confirm password: ADMIN
Superuser was successfully created
(venv) developer@MacBook-Pro auth % flask create-superuser ADMIN@email.com
User already exists. Try again with another email

```
### Миграции

Чтобы накатить миграции, необходимо выполнить команду:
- `flask db upgrade` при локальной разработке;
- `docker exec -ti auth flask db upgrade` в поднятом докер контейнере;

## 🗃 4. Бэкенд с возможностью управления профилями пользователей, в том числе аватарки, а также добавление избранного, оценок, ревью и лайков (Backend).
Сервис содержит основную логику CRUD работы с профилем пользователя

Коллекция с основными ручками лежит в папке ./backend/backend.postman_collection.json

- Для просмотра всех пользователей под учетной записью администратора необходимо следующее:
1. Создать суперпользователя в сервисе auth
2. Авторизоваться суперпользователем в сервисе auth и сохранить access_token.
2. Зарегистрировать нового пользователя в backend с помощью запроса, например
```commandline
curl --location --request POST '127.0.0.1:8000/v1/user/register' \
--header 'user_uuid: d16b19e7-e116-43b1-a95d-cd5a11e8f1b7' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "user000@email.com",
    "password": "user000",
    "password_confirmation": "user000",
    "first_name": "Олег",
    "family_name": "Иванов",
    "father_name": "Борисович",
    "phone": "+79104470000"
}'
```
3. С помощью роли суперпользователя в сервисе Auth создать роль "Admin"
```commandline
curl --location --request POST 'http://0.0.0.0:5001/api/v1/user/roles' \
--header 'Authorization: {access_token} \
--header 'Content-Type: application/json' \
--data-raw '{"name": "Admin"}'
```
4. Авторизоваться зарегистрированным пользователем через сервис Auth и сохранить access_token
```commandline
curl --location --request POST '0.0.0.0:5001/api/v1/user/login' \
--header 'Content-Type: application/json' \
--data-raw '{"email": "user000@email.com", "password": "user000"}'
```
5. Узнать user_id зарегистрированного пользователя, используя метод просмотра данных о личном профиле. Токен взять из предыдущего шага.
```commandline
curl --location --request GET '127.0.0.1:8000/v1/user/get-profile' \
--header 'Authorization: Bearer {access_token}' \
--data-raw ''
```
6. Присвоить новому пользователю по user_id роль admin, используя токен суперпользователя
```commandline
curl --location --request POST 'http://0.0.0.0:5001/api/v1/user/user-role' \
--header 'Authorization: Bearer {access_token}' \
--header 'Content-Type: application/json' \
--data-raw '{
    "user_id": "6a1385cb-c0b8-4fd3-884c-d3399bd9c98e",
    "role_id": "d2bb61f5-a681-4b25-8961-1a3d1a3ad3e1"
}'
```
7. Теперь новый пользователь является админом и может просматривать все профили. Для просмотра всех пользователей необходимо передать параметр user_id со значением ["*"] В метод добавлена пагинация. 
```commandline
curl --location --request GET '127.0.0.1:8000/v1/user/profiles?page=1&size=4' \
--header 'Content-Type: application/json' \
--data-raw '{   
    "email": "user555@email.com",
    "password": "user000",
    "users_id": ["*"]
}'
```

## 🙍‍♂️ 5.Сервис для взаимодействия с данными профилей (Profiles)
Сервис реализован через технологию gRPC. 

Файлы в ./profiles/src/grpc_files генерируются автоматически на основе файла ./profiles/protos/profiles.proto. 

Если потребуется отредактировать ./profiles/protos/profiles.proto, то после этого нужно заново сгенерировать файлы в ./profiles/src/grpc_files. Для этого достаточно запустить скрипт update_protos.sh

Сервис будет работать асинхронно, если глобальная переменная **RUN_MODE** будет содержать значение **ASYNC**. 

Логику для запуска сервиса можно посмотреть в файле ./profiles/src/entrypoint.sh

Для запуска локального тестового клиента можно воспользоваться файлом ./profiles/src/profiles_client_sample.py. 

Также доступны тесты в папке ./profiles/tests

## 6. Сервис UGC (лайки, рецензии и т. д.)
Если не указан user id, то он берётся из заголовков авторизации. 

1. Добавить лайк к фильму
```commandline
curl --request POST '127.0.0.1:8000/v1/likes/add' \
--header 'Content-Type: application/json' \
--data-raw '{   
    "movie": "803c794c-ddf0-482d-b2c2-6fa92da4c5e2",
    "value": 5
}'
```

2. Удалить лайк к фильму
```commandline
curl --request DELETE '127.0.0.1:8000/v1/likes/remove' \
--header 'Content-Type: application/json' \
--data-raw '{   
    "id": "803c794c-ddf0-482d-b2c2-6fa92da4c5e2"
}'
```
id = movie id. 

3. Посчитать лайки к фильму
```commandline
curl --request GET '127.0.0.1:8000/v1/likes/count' \
--header 'Content-Type: application/json' \
--data-raw '{   
    "id": "803c794c-ddf0-482d-b2c2-6fa92da4c5e2"
}'
```

4. Добавить рецензию к фильму
```commandline
curl --request POST '127.0.0.1:8000/v1/likes/count' \
--header 'Content-Type: application/json' \
--data-raw '{   
    "movie": "803c794c-ddf0-482d-b2c2-6fa92da4c5e2",
    "text" : "......"
}'
```

5. Удалить рецензию к фильму
```commandline
curl --request DELETE '127.0.0.1:8000/v1/likes/count' \
--header 'Content-Type: application/json' \
--data-raw '{   
    "id": "53954284-caaf-4248-b0e7-fd1265499a91"
}'
```

6. Получить рецензию к фильму
Берётся по user id из авторизации.
```commandline
curl --request GET '127.0.0.1:8000/v1/reviews/get' \
--header 'Content-Type: application/json' \
--data-raw '{   
    "id": "803c794c-ddf0-482d-b2c2-6fa92da4c5e2"
}'
```

7. Получить все список всех рецензий к фильму
```commandline
curl --request GET '127.0.0.1:8000/v1/reviews/list' \
--header 'Content-Type: application/json' \
--data-raw '{   
    "id": "803c794c-ddf0-482d-b2c2-6fa92da4c5e2"
}'
```

8. Добавить лайк к рецензии
```commandline
curl --request POST '127.0.0.1:8000/v1/review_likes/add' \
--header 'Content-Type: application/json' \
--data-raw '{   
    "review": "63ff480aa96c3ea499bc01242",
    "movie":  "803c794c-ddf0-482d-b2c2-6fa92da4c5e2",
    "review_author_id": "d96f4d59-12d4-419c-967d-fd62c41cc6b0",
    "value": 5
}'
```
9. Удалить лайк к рецензии
```commandline
curl --request DELETE '127.0.0.1:8000/v1/review_likes/remove' \
--header 'Content-Type: application/json' \
--data-raw '{   
    "id": "620934552b431a95fdcd7c7ca"
}'
```

10. Получить количество лайков к рецензии
```commandline
curl --request GET '127.0.0.1:8000/v1/review_likes/count' \
--header 'Content-Type: application/json' \
--data-raw '{   
    "id": "63ff480aa96c3ea499bc01242"
}'
```

11. Добавить закладку
```commandline
curl --request POST '127.0.0.1:8000/v1/bookmarks/add' \
--header 'Content-Type: application/json' \
--data-raw '{   
    "movie": "803c794c-ddf0-482d-b2c2-6fa92da4c5e2"
}'
```

12. Удалить закладку
```commandline
curl --request DELETE '127.0.0.1:8000/v1/bookmarks/remove' \
--header 'Content-Type: application/json' \
--data-raw '{   
    "movie": "803c794c-ddf0-482d-b2c2-6fa92da4c5e2"
}'
```

13. Получить список закладок
```commandline
curl --request POST '127.0.0.1:8000/v1/bookmarks/list' \
--header 'Content-Type: application/json' \
--data-raw '{   
    "movie": "803c794c-ddf0-482d-b2c2-6fa92da4c5e2"
}'
```



