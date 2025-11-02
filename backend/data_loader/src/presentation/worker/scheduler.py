from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource


def init_scheduler(broker) -> TaskiqScheduler:
    return TaskiqScheduler(
        broker=broker,
        sources=[LabelScheduleSource(broker)],
    )
