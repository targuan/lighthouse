# Lighthouse
### Running
Install the requirements

```python manage.py collectstatic```
```gunicorn --bind 0.0.0.0:8000 lighthouse.wsgi --reload --log-file -```
```celery -A lighthouse worker -l INFO```
