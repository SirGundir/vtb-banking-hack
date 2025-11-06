from app_instance import broker
from presentation.worker.scheduler import init_scheduler

scheduler = init_scheduler(broker)
