# Docker конфигурация для VTB Banking Hack Frontend

## Структура
- `Dockerfile` - основной файл для сборки Docker образа
- `docker-compose.yml` - конфигурация для запуска контейнера
- `.dockerignore` - файлы исключаемые из Docker образа

## Технологии
- **Сборщик**: Bun (используется `oven/bun:1-alpine` для сборки)
- **Production сервер**: Nginx Alpine
- **Порт**: 80

## Сборка и запуск

### Сборка образа
```bash
make docker-build
```

### Запуск через Docker Compose
```bash
make docker-up
```

### Запуск через Docker напрямую
```bash
make docker-run
```

### Остановка контейнера
```bash
make docker-down
```

## Переменные окружения

### Переменные для runtime
После сборки фронтенд представляет собой статические файлы, которые обслуживаются Nginx. Переменные окружения в `docker-compose.yml` (`NODE_ENV`, `VITE_HOST`, `VITE_PORT`, `VITE_CLIENT_ID`, `VITE_CLIENT_SECRET`) используются только для информации и не влияют на работу собранного приложения.

## Примеры использования

### Разработка

Используйте команды Makefile для удобной работы с Docker:

```bash
# Запуск в фоновом режиме
make docker-up

# Просмотр логов
make docker-logs

# Перезапуск после изменений
make docker-restart

# Остановка контейнера
make docker-down
```

### Пересборка образа

```bash
# Пересборка и запуск
make docker-rebuild
```

### Все доступные Docker команды

```bash
make docker-up          # Запуск контейнера в фоновом режиме
make docker-down        # Остановка и удаление контейнера
make docker-logs        # Просмотр логов (с флагом -f для следования)
make docker-restart     # Перезапуск контейнера
make docker-rebuild     # Пересборка образа и запуск
make docker-build       # Только сборка образа
make docker-run         # Запуск через docker run
make docker-stop        # Остановка и удаление контейнера (альтернатива)
```

Или используйте команды напрямую через Docker Compose:

```bash
# Запуск в фоновом режиме
docker-compose -f docker/docker-compose.yml up -d

# Просмотр логов
docker-compose -f docker/docker-compose.yml logs -f

# Перезапуск после изменений
docker-compose -f docker/docker-compose.yml restart

# Пересборка образа
docker-compose -f docker/docker-compose.yml build --no-cache
docker-compose -f docker/docker-compose.yml up -d
```

## Структура Dockerfile

Dockerfile использует multi-stage сборку:

1. **Stage builder** (`oven/bun:1-alpine`): 
   - Установка зависимостей через `bun install --frozen-lockfile`
   - Сборка приложения через `bun -bun run build`

2. **Stage production** (`nginx:alpine`):
   - Копирование собранных файлов из `dist` в `/usr/share/nginx/html`
   - Настройка Nginx для обслуживания статических файлов
   - Запуск через `dumb-init` для корректной обработки сигналов
