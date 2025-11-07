from core.dto import BaseModelDTO


def dto_to_ndjson(objs: list[BaseModelDTO]) -> str:
    return '\n'.join(obj.model_dump_json() for obj in objs)
