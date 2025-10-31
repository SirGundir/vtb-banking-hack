## Запустить проект

### Энвсы:

- `postgres/.env`
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=vtb_banking.postgres
POSTGRES_PORT=5432
POSTGRES_DATABASE=postgres
```

- user_api/.env
```
REDIS_PORT=6379
REDIS_HOST=vtb_banking.redis
SECRET_KEY='wow so secret'
```

### Запуск:
```
make down ; make build ; make up
# После старта заинитить БД
make head
```

Запустится на 4000 порту.

### Выгрузить API доку:
```
make user_api_docs
```