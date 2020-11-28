# Проект Yamdb

Yamdb - это база отзывов о фильмах, книгах и музыке. Здесь пользователь может оставить отзыв (Review) и выставить рейтинг произведению (Title). 
Произведения делятся на категории: «Книги», «Фильмы», «Музыка». При этом список категорий (Category) может быть расширен. Сами произведения в YaMDb не хранятся.

В сервисе есть следующие пользовательские роли:
- Аноним — может просматривать описания произведений, читать отзывы и комментарии.
- Аутентифицированный пользователь (user)— может читать всё, как и Аноним, дополнительно может публиковать отзывы и ставить рейтинг произведениям (фильмам/книгам/песням), может комментировать чужие отзывы и ставить им оценки; может редактировать и удалять свои отзывы и комментарии.
- Модератор (moderator) — те же права, что и у Аутентифицированного пользователя плюс право удалять любые отзывы и комментарии.
- Администратор (admin) — полные права на управление проектом и всем его содержимым. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
- Администратор Django — те же права, что и у роли Администратор.

Yamdb использует следующий алгоритм регистрации пользователей:
- Пользователь отправляет POST-запрос с параметром email на /api/v1/auth/email/.
- YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес email .
- Пользователь отправляет POST-запрос с параметрами email и confirmation_code на /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен).

Эти операции выполняются один раз, при регистрации пользователя. В результате пользователь получает токен и может работать с API, отправляя этот токен с каждым запросом.
После регистрации и получения токена пользователь может отправить PATCH-запрос на /api/v1/users/me/ и заполнить поля в своём профайле.

Ресурсы API YaMDb:
- Ресурс AUTH: аутентификация.
- Ресурс USERS: пользователи.
- Ресурс TITLES: произведения, к которым пишут отзывы (определённый фильм, книга или песня).
- Ресурс CATEGORIES: категории (типы) произведений («Фильмы», «Книги», «Музыка»).
- Ресурс GENRES: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
- Ресурс REVIEWS: отзывы на произведения. Отзыв привязан к определённому произведению.
- Ресурс COMMENTS: комментарии к отзывам. Комментарий привязан к определённому отзыву.

## Используемые технологии

- Python
- Django
- Django Rest Framework
- PostgreSQL
- Docker
- Docker compose

## Запуск и использование

Для того, чтобы все заработало, выполните описанные ниже действия.

### Команды для запуска

Для запуска необходимо выполнить всего одну команду из директории приложения (там, где лежат файлы Dockerfile и docker-compose.yaml):

```
docker-compose up
```
Готово! Вы великолепны!

### Команда для создания суперпользователя

Для того, чтобы создать суперпользователя, необходимо войти в контейнер **infra_sp2_web_1**:

```
docker exec -it <CONTAINER ID> bash
```
Чтобы узнать CONTAINER ID:

```
docker container ls -all
```  
Далее выполняем:

```
python manage.py createsuperuser
```  
Вводим e-mail и пароль. Суперпользователь создан.

### Заполнение базы начальными данными

Начальные данные лежат в файле fixtures.json.
Для того, чтобы заполнить базу, необходимо войти в контейнер **infra_sp2_web_1** (как это сделать указано в п. "Команда для создания суперпользователя") и выполнить команду:

```
python manage.py loaddata fixtures.json
```

### Как пользоваться ресурсом

После запуска правила пользования доступны по адресу http://localhost/redoc/.

### Другие полезные команды:

Создать миграцию (сгенерировать команды SQL):

```
python manage.py makemigrations
```
Запустить миграцию (выполнить команды SQL):

```
python manage.py migrate
```

![yamdb workflow](https://github.com/gooncharova/yamdb_final/workflows/yamdb_workflow/badge.svg)
