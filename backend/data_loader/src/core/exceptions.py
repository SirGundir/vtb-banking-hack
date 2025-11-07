class DetailedError(Exception):
    default_message = None

    def __init__(self, detail=None, *args, silent=False, source=None, **kwargs):
        self.source = source
        self.detail = detail or self.default_message
        self.silent = silent
        super().__init__(detail)


class ValidateDataError(DetailedError):
    """Validation data error"""


class ActionNotAllowedError(DetailedError):
    """Action not allow."""