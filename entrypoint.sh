#!/bin/bash
set -e


#echo "Ensuring static directory exists..."
## Создаем папку, если её нет
#mkdir -p /home/rec_shop/static
#
## Если ваши статические файлы лежат внутри папки app/static,
## их нужно скопировать в volume, чтобы Nginx их увидел:
#if [ -d "/home/rec_shop/app/static" ]; then
#    echo "Syncing static files..."
#    cp -r /home/rec_shop/app/static/. /home/rec_shop/static/
#fi


echo "Applying migrations..."
alembic upgrade head

echo "Starting server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000