web: gunicorn application.wsgi
worker: celery worker -B -l info -A application.celery