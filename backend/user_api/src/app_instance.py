from api.app import init_app, lifespan
from config import settings


app = init_app(lifespan, no_db_routing_urls=settings.NO_DB_ROUTING_URLS)
