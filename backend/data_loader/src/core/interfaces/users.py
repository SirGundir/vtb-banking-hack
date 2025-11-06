from core.dto import UserAccountDTO
from core.interfaces.data_loaders import LoaderInterface, Credentials


class UserAccountsLoaderInterface(LoaderInterface):

    async def get_page(self, credentials: Credentials, page=None) -> list[UserAccountDTO]:
        raise NotImplementedError