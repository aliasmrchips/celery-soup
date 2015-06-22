CELERY_IGNORE_RESULT = False

CELERYD_MAX_TASKS_PER_CHILD = 2

BROKER_URL = 'redis://localhost:6379/0'

CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

CELERY_ROUTES = {'soup.map': {'queue': 'soup'}, 'soup.reduce': {'queue': 'soup'}}