# Информационная система управления недвижимостью

Стек: **React** (frontend), **Django REST Framework** (backend), **PostgreSQL**, развертывание в **Docker**.

## Возможности

- Объекты недвижимости (типы, статусы, удобства)
- Арендаторы и договоры аренды
- Платежи (аренда, коммунальные и др.)
- Заявки на обслуживание с комментариями
- Отчеты и экспорт в CSV/Excel (для администратора/менеджера)
- Журнал аудита и управление пользователями (для администратора)
- Роли: администратор, менеджер, арендатор

## Запуск через Docker (рекомендуется)

### Требования

- Установленные [Docker](https://docs.docker.com/get-docker/) и [Docker Compose](https://docs.docker.com/compose/install/)

### Шаги

1. Клонируйте репозиторий и перейдите в каталог проекта:
   ```bash
   cd c:\Users\goonthug\PycharmProjects\PythonProject3
   ```

2. Создайте файл с переменными окружения (один раз):
   ```bash
   copy .env.example .env
   ```
   При необходимости отредактируйте `.env` (пароль БД, `SECRET_KEY` и т.д.).

3. Соберите образы и запустите контейнеры:
   ```bash
   docker-compose up --build -d
   ```

4. Дождитесь запуска (около 30–60 секунд). При первом запуске выполняются миграции и заполнение тестовыми данными.

5. Откройте в браузере:
   - **Фронтенд (интерфейс):** http://localhost:3000
   - **Бэкенд API (документация):** http://localhost:8000/api/docs/

### Учетные данные по умолчанию (после seed)

| Роль      | Email               | Пароль    |
|-----------|---------------------|-----------|
| Админ     | admin@property.ru   | admin123  |
| Менеджер  | manager@property.ru | manager123|
| Арендатор | tenant1@mail.ru    | tenant123 |

### Остановка

```bash
docker-compose down
```

Данные БД сохраняются в Docker-томе. Чтобы удалить и их:

```bash
docker-compose down -v
```

---

## Запуск без Docker (разработка)

### Бэкенд

1. Установите PostgreSQL и создайте БД и пользователя (как в `.env`).

2. В каталоге `backend`:
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   copy ..\.env.example .env
   ```
   Заполните `.env`: укажите `POSTGRES_HOST=localhost` и реальные пароли.

3. Миграции и тестовые данные:
   ```bash
   python manage.py migrate
   python manage.py seed_data
   ```

4. Запуск сервера:
   ```bash
   python manage.py runserver
   ```
   API: http://localhost:8000

### Фронтенд

1. В каталоге `frontend`:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   Интерфейс: http://localhost:3000 (прокси к API на порт 8000 настроен в `vite.config.js`).

---

## Структура проекта

```
PythonProject3/
  docker-compose.yml    # Сервисы: db, backend, frontend
  .env.example
  backend/
    config/             # Настройки Django
    apps/
      users/            # Авторизация, JWT, пользователи
      properties/       # Объекты недвижимости
      tenants/          # Арендаторы и договоры
      payments/         # Платежи и категории
      service_requests/ # Заявки на обслуживание
      audit/            # Журнал аудита
      reports/         # Отчеты и экспорт
    manage.py
    requirements.txt
    Dockerfile
    entrypoint.sh
  frontend/
    src/
      api/              # HTTP-клиент (axios)
      context/          # AuthContext
      components/
      pages/
    index.html
    package.json
    vite.config.js
    Dockerfile
    nginx.conf
```

После перезагрузки страницы сессия не сбрасывается: используется JWT (access + refresh), токены хранятся в `localStorage`, refresh выполняется автоматически.
