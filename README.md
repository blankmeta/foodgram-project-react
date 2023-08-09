# Foodgram

# Запуск:

### Поднимите контейнеры в директории ./infra
```
docker-compose up -d --build
```
### Заполните базу ингредиентами и тегами
```
docker-compose exec -T backend python manage.py fill_ingredients ingredients.json
docker-compose exec -T backend python manage.py fill_tags tags.json
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
