# praktikum_new_diplom

```
Ip - http://84.201.178.138/
Логпасс админки - root:root
Пользователи - admin@gmail.com:admin, aboba@gmail.com:aboba
```

# Запуск:

### Поднимите контейнеры в директории ./infra
```
docker-compose up -d --build
```

# Шаблон наполнения .env
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=user
POSTGRES_PASSWORD=pass
DB_HOST=db
DB_PORT=5432
DEBUG=False
SECRET_KEY=your_secret_key
```
