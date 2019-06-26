from typing import List, Tuple

from infrastructure.repository import BaseRepository
from .model import Service


class ServiceRepository(BaseRepository[Service]):
    def __init__(self, **kwargs):
        super().__init__(Service, **kwargs)

    def get_service_list(self,
                          query_string: str) -> Tuple[List[Service], int]:

        return self.consume_search(query_string)
