# test_api_for_answer_and_question

## Описание проекта 🌓

*По любым вопросам по коду, писать в телеграмм, который указан в конце документа
---

### Шаги установки 🚀
1. **Склонируйте репозиторий**:
```bash
    git clone https://github.com/gol43/test_api_for_answer_and_question.git

    cd test_api_for_answer_and_question
```

2. **Создайте и активируйте виртуальное окружение**:
```bash
    python -m venv venv

    source venv/bin/activate
```

3. **Установите зависимости**:
```bash
    pip install -r requirements.txt
```

---

### Примеры запуска 🧰

1. **Создать файл .env в корне с данными (пример)** ⚙️
```bash
POSTGRES_USER=postgres
POSTGRES_PASSWORD=1234
POSTGRES_DB=test_hightalent_db
POSTGRES_HOST=db
POSTGRES_PORT=5432
DATABASE_URL=postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}
```

2. **Создание образов и запуск контейнера** 🐳
```bash
docker compose up -d
```

3. **Создание миграций и их применение** 🌱
```bash
docker exec -it hightalent_app bash

alembic revision --autogenerate -m "initial"

alembic upgrade head
```

4. **Работа с проектом**

- Нужно перейти по ссылке swagger: http://127.0.0.1:8000/api/v1/hightalent/docs#/

- Зарегестрируйте пользователя по ссылке /api/v1/auth/register/
вот пример запроса:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/auth/register/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=gol43&password=1234'
  ```

- Далее нужно аутентифицироваться и получить jwt-token:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/auth/login/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=gol43&password=1234'
  ```

- Из ответа нужно скопировать токен и вставить его в Value для кнопки Authorize
![alt text](image.png)
вот пример ответа при логировании:
```bash
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJnb2w0MyIsInVzZXJuYW1lIjoiZ29sNDMiLCJleHAiOjE3NjMzODM5OTIsImlhdCI6MTc2MzM4MzM5Mn0.PTEu11b-ssIX27MIWjhftJxjEtWSsFOVNHdMbGAqaSA6HDSjFS6eSECcPMQXHBj5NSP73Z5NxGyN4U5Z6pNCOSbhzpEAFcvPlQS6g6vH-51LUR6mP_pvqZwgEDfn7zKGTlArdkRr5KZwXOIZ_JfdEsIk1U33_m8cNnxZFxwXk56sp3KyRd862ei2YbpM41WKDDxaE6mBgNWWSx8ErOasEiX-lvQEQP7_Qj46mFJp9MRwBityZSzlDp1ypa4enziehoDCF8wLH6kb20lr3599gGJ1D954RiygIV9lnP4YfF2ElEQtvL9Mh3EjdL_0bUjNij0N6FRKif19tCDUUqheMw",
  "token_type": "Bearer",
  "username": "gol43"
}
```

- После аутентификация можно спокойно пользоваться сервисом - создавать вопросы и ответы, а также пользоваться всеми нужными CRUD запросами.


--- 

## 👨‍💻 Автор

Проект разработан:  
**Сайгушев Дамир Даниярович**  
- GitHub: [gol43](https://github.com/gol43)  
- Telegram: [@spongedmw](https://t.me/spongedmw)

---
