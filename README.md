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
API Docs: http://localhost:8000/docs
Grafana: http://localhost:3000 (логин/пароль: admin/admin) — бизнес-метрики и тех. состояние.  
Flower: http://localhost:5555 — статус фоновых задач Celery.  
Prometheus: http://localhost:9090 — сырые метрики.  
GlitchTip  http://localhost:8080/ мониторинга ошибок и производительности  

⚙️ Переменные окружения (.env)  
Создайте файл .env на основе примера:  
```.env
# App
APP_NAME=RecommendationsAPI
MODE=DEV
LOG_LEVEL=INFO

# Auth
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/recs_db
```
Создайте файл .docker.env на основе примера:  
```.docker.env
# App
APP_NAME=RecommendationsAPI
MODE=PROD
LOG_LEVEL=INFO

# Auth
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL=postgresql+asyncpg://user:password@db:5432/recs_db
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

Для проверки покрытия логов и моков:
```bash
uv run pytest -s -vv
```




