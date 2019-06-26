from typing import List, Tuple

from infrastructure.repository import BaseRepository
from .model import Category


class CategoryRepository(BaseRepository[Category]):
    def __init__(self, **kwargs):
        super().__init__(Category, **kwargs)

    def get_category_list(self,
                          query_string: str) -> Tuple[List[Category], int]:
        return self.consume_search(query_string)
