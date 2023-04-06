Для запуска миграций необходимо:
- `docker exec -ti admin_panel_async_api python manage.py migrate`
- `docker exec -ti auth flask db upgrade`