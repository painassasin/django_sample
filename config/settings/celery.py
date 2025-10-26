from .base import IS_TESTING, REDIS_HOST, REDIS_PORT, TIME_ZONE, env

CELERY_DB = env.int('CELERY_DB', 0)

CELERY = {
    'broker_url': f'redis://{REDIS_HOST}:{REDIS_PORT}/{CELERY_DB}',
    'task_always_eager': IS_TESTING,
    'task_eager_propagates': IS_TESTING,
    'timezone': TIME_ZONE,
    'worker_concurrency': env.int('CELERY_WORKER_CONCURRENCY', 1),
}
