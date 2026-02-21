@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo === ИСУН: подготовка и запуск ===

if not exist .env (
  echo Создаю .env из .env.example...
  copy .env.example .env >nul
  echo Файл .env создан. При необходимости отредактируйте его.
) else (
  echo Файл .env уже существует.
)

where docker >nul 2>nul
if errorlevel 1 (
  echo Ошибка: Docker не найден. Установите Docker Desktop.
  pause
  exit /b 1
)

docker info >nul 2>nul
if errorlevel 1 (
  echo Ошибка: Docker не запущен. Запустите Docker Desktop.
  pause
  exit /b 1
)

echo Запуск контейнеров...
docker compose up --build -d

echo.
echo Контейнеры запущены. Подождите 30-60 сек.
echo   Фронтенд:  http://localhost:3000
echo   API/docs:  http://localhost:8000/api/docs/
echo.
echo Остановка: docker compose down
pause
