from typing import Annotated

from fastapi import Depends, Request

from infrastructure.di.di_container import DIContainer


def get_di_container(request: Request):
    return request.state.di_container


di_container_dep = Annotated[DIContainer, Depends(get_di_container)]
