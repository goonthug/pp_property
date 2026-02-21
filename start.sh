#!/usr/bin/env bash
# Запуск проекта ИСУН (Docker): зависимости, .env, миграции, контейнеры.
# Использование: ./start.sh   (Linux/Mac)

set -e
cd "$(dirname "$0")"

echo "=== ИСУН: подготовка и запуск ==="

if [ ! -f .env ]; then
  echo "Создаю .env из .env.example..."
  cp .env.example .env
  echo "Файл .env создан. При необходимости отредактируйте его (пароль БД, SECRET_KEY)."
else
  echo "Файл .env уже существует."
fi

if ! command -v docker &>/dev/null; then
  echo "Ошибка: Docker не найден. Установите Docker: https://docs.docker.com/get-docker/"
  exit 1
fi

if ! docker info &>/dev/null; then
  echo "Ошибка: Docker не запущен или нет доступа. Запустите Docker Desktop (или демон docker)."
  exit 1
fi

echo "Запуск контейнеров (сборка при первом запуске)..."
docker compose up --build -d

echo ""
echo "Контейнеры запущены. Подождите 30–60 сек. пока поднимется БД и бэкенд."
echo ""
echo "  Фронтенд:  http://localhost:3000"
echo "  API/docs:  http://localhost:8000/api/docs/"
echo ""
echo "Остановка: docker compose down"
