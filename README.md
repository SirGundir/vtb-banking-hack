# vtb-banking-hack

## Запустить проект

### Энвсы:

- `backend/postgres/.env`
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=vtb_banking.postgres
POSTGRES_PORT=5432
POSTGRES_DATABASE=postgres
```

- `backend/user_api/.env`
```
REDIS_PORT=6379
REDIS_HOST=vtb_banking.redis
SECRET_KEY='wow so secret'
```

- `frontend/.env`
```
# ToDo
```

### Запуск frontend + api:
```
make down_dev ; make build_dev ; make up_dev
# После старта заинитить БД
make db_head
```

### Запуск только бека:
```
make down_be ; make build_be ; make up_be
```

### Выгрузить API доку:
```
make user_api_docs
```