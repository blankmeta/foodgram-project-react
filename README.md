# praktikum_new_diplom


# Запуск:

### Поднимите контейнеры в директории ./infra
```
docker-compose up -d --build
```

### Заполните теги и ингредиенты в базу:
```
docker-compose exec backend python manage.py fill_tags tags.json
docker-compose exec backend python manage.py fill_ingredients ingredients.json
```
