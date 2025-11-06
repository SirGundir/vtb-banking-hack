from presentation.worker.app import init_app, app_lifespan
from presentation.worker.broker import init_broker


app = init_app(init_broker, lifespan=app_lifespan)
