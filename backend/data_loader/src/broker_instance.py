from infrastructure.config.redis import RedisConfig
from presentation.worker.broker import init_broker


broker = init_broker(RedisConfig())
