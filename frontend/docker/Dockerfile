# Базовый образ для сборки
FROM oven/bun:1-alpine AS builder

# Установка рабочей директории
WORKDIR /app

# Копирование всего проекта
COPY . .

# Установка зависимых с выполнением скриптов
RUN bun install --frozen-lockfile

# Сборка приложения с переменными окружения
RUN bun -bun run build

# Production образ
FROM nginx:alpine AS production

# Установка dumb-init для корректной обработки сигналов
RUN apk add --no-cache dumb-init

# Создание необходимых директорий для nginx с правильными правами
RUN mkdir -p /var/cache/nginx/client_temp \
    /var/cache/nginx/proxy_temp \
    /var/cache/nginx/fastcgi_temp \
    /var/cache/nginx/uwsgi_temp \
    /var/cache/nginx/scgi_temp \
    /var/run && \
    chown -R nginx:nginx /var/cache/nginx \
    /var/run \
    /var/log/nginx \
    /usr/share/nginx/html \
    /etc/nginx/conf.d

# Копирование собранного приложения из builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Копирование конфигурации nginx (если нужно)
# COPY nginx.conf /etc/nginx/nginx.conf

# Установка прав пользователя
RUN chown -R nginx:nginx /usr/share/nginx/html

# Открытие порта
EXPOSE 80

# Переменные окружения
ENV NODE_ENV=production

# Запуск nginx с dumb-init
ENTRYPOINT ["dumb-init", "--"]
CMD ["nginx", "-g", "daemon off;"]
