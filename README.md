# RecommendationsAPI

Магазин с интеллектуальной рекомендательной системой на основе алгоритмов совместных покупок (Matrix Lift).

## 🚀 Технологический стек
*   **Backend:** FastAPI, SQLAlchemy (Async), Celery
*   **Database:** PostgreSQL (основная), Redis (брокер задач)
*   **Tooling:** `uv` (управление пакетами), Alembic (миграции)
*   **QA:** Pytest (Async), Ruff (линтер), Mypy (типизация)


## 🛠 Установка и запуск

## Вариант 1: Локально через `uv`
Для разработки и запуска тестов:
### Установка зависимостей
```bash
uv sync
```
### Активация окружения на UNIX-системах
```
source .venv/bin/activate 
``` 
### Активация окружения на Windows
```
.venv\Scripts\activate 
```
### Запуск миграций
```
uv run alembic upgrade head
```

### Запуск API
```
uv run uvicorn app.main:app --reload
```


## Вариант 2: Через Docker Compose (Production-ready)  
Поднимает весь стек: API, Worker, DB, Redis.
```bash
docker compose up -d --build
```


📊 Мониторинг и управление  
После запуска доступны следующие интерфейсы:  
API Docs: http://localhost/docs 
Grafana: http://localhost/grafana/ (логин/пароль: admin/admin) — бизнес-метрики и тех. состояние.  
Flower: http://localhost/flower/ — статус фоновых задач Celery.  
Prometheus: http://localhost/prometheus/ — сырые метрики.  
GlitchTip  http://gt.localhost/ мониторинга ошибок и производительности  

⚙️ Переменные окружения (.env)  
Создайте файл .env на основе примера:  
```.env
# --- НАСТРОЙКИ ВАШЕГО ПРИЛОЖЕНИЯ ---
APP_NAME="RecommendationsAPI"
MODE=PROD
LOG_LEVEL="INFO"

APP_POSTGRES_DB=recs_db
APP_POSTGRES_USER=user
APP_POSTGRES_PASSWORD=password
# Ссылка на сервис app-db 
DATABASE_URL=postgresql+asyncpg://user:password@app-db:5432/recs_db

# --- НАСТРОЙКИ GLITCHTIP ---
GT_POSTGRES_DB=glitchtip
GT_POSTGRES_USER=glitchtip
GT_POSTGRES_PASSWORD=glitchtip_pass
# Ссылка на сервис gt-db
GT_DATABASE_URL=postgres://glitchtip:glitchtip_pass@gt-db:5432/glitchtip

# Общий Redis для всех
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0

# GlitchTip Config

#GLITCHTIP_DOMAIN=http://localhost/gt
#SENTRY_DSN=http://3d1605aa00a74cf3ad4c38ee3ef187ff@gt.localhost/1
# SENTRY_DSN=http://3d1605aa00a74cf3ad4c38ee3ef187ff@nginx/gt/1
# Регистрация (True только для создания первого админа, потом ставь False)
#ENABLE_OPEN_USER_REGISTRATION=False
#SECURE_SSL_REDIRECT=False

# Остальное
LOKI_URL=http://loki:3100/loki/api/v1/push

SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

🏗 Архитектура системы  
FastAPI принимает заказ и инициирует checkout.  
Celery Worker в фоновом режиме пересчитывает матрицу рекомендаций (Lift), используя CTE-запросы в БД.  
🔄 CI/CD  
Проект включает автоматизированный пайплайн:  
Linting: Ruff проверяет стиль кода и сортировку импортов.  
Types: Mypy проверяет статическую типизацию.  
Tests: Pytest запускает асинхронные тесты в изолированной SQLite.  

🧪 Тестирование
```bash
uv run pytest
```





