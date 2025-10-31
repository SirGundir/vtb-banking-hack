from sqlalchemy.exc import DatabaseError

from core.exceptions import DetailedError


class DoesNotExists(DetailedError):
    """Record doesn not exists"""


class AlreadyExistsError(DetailedError):
    """Record already exists"""


def raise_from_pg_error(exc: DatabaseError, silent: bool = False):
    pg_code = getattr(exc.orig, 'pgcode')
    match pg_code:
        case '23505':
            # unique_violation
            raise AlreadyExistsError(
                detail=f"Already exists.",
                source=exc,
                silent=silent
            )
        case _:
            raise exc
