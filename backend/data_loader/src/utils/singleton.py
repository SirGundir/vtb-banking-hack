class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        key = f"{cls.__name__}{args}{kwargs}"
        if key not in cls._instances:
            cls._instances[key] = super().__call__(*args, **kwargs)
        return cls._instances[key]
