BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'Europe/Oslo'
CELERY_ENABLE_UTC = True

CELERY_IMPORTS = ['flgproc.%s' % x for x in [
    'filter.duplicate',
    'filter.matching',

    'collector.demo',
    'submitter.demo',
]]

CELERY_ROUTES = {
    'flgproc.submitter.submit_flag': {'queue': 'submit'}
}