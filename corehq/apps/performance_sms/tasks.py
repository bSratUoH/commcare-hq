from celery.schedules import crontab
from celery.task import periodic_task
from .models import PerformanceConfiguration
import settings


@periodic_task(run_every=crontab(hour="*/1", minute="0"), queue=getattr(settings, 'CELERY_PERIODIC_QUEUE', 'celery'))
def daily_reports():
    for config in PerformanceConfiguration.get_message_configs_at_this_hour():
        config.fire_messages()
