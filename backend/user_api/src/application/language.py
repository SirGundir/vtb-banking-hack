from collections import UserDict

from core.exceptions import ValidateDataError


class Langs(UserDict):
    def validate_code(self, lang_code: str):
        if lang_code not in self:
            raise ValidateDataError(detail='Not valid value for language')
        return lang_code


LANGUAGES = Langs(
    en="English",
    es="Español",
    fr="Français",
    pt="Português",
    ar="العربية",
    hi="हिन्दी",
    ja="日本語",
    zh="中文",
    it="Italiano",
    de="Deutsch"
)
