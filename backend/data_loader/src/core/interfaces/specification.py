from abc import ABC


class SpecificationInterface(ABC):

    def apply_fields(self, fields):
        return fields

    def apply(self, select_query):
        return select_query


class OnConflictInterface(ABC):

    def apply_conflict(self, insert_query):
        raise NotImplementedError
