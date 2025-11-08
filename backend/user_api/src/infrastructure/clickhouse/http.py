import aiohttp
from aiochclient import ChClient

from infrastructure.config.clickhouse import ClickhouseConfig
from utils.event_loop import safe_get_loop


class ClickhouseClientSession(aiohttp.ClientSession):
    """Class to split dependencies"""


def init_clickhouse_client(config: ClickhouseConfig) -> ChClient:
    loop = safe_get_loop()
    session = aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(
            loop=loop,
            **config.connection_config
        )
    )
    return ChClient(session, **config.clickhouse_params)
