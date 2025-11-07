FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем requirements и устанавливаем зависимости
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем приложение
COPY ./app /app

# Создаем директорию для моделей
RUN mkdir -p /app/ml_model/saved_models && \
    chmod -R 777 /app/ml_model/saved_models

# Проверка установки
RUN python -c "import catboost; import gensim; print('Dependencies OK')"

# Запуск
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]