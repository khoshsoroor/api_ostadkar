from typing import List, Tuple

from sqlalchemy.orm import joinedload

from infrastructure.repository import BaseRepository
from .model import Provide


class ProvideRepository(BaseRepository[Provide]):
    def __init__(self, **kwargs):
        super().__init__(Provide, **kwargs)

    def get_provide_list(self, query_string: str) -> Tuple[List[Provide], int]:
        return self.consume_search(query_string,
                                   opt=lambda x: x.options(joinedload(Provide.service, innerjoin=True),
                                                           joinedload(Provide.city, innerjoin=True)),
                                   opt2=lambda x: x)

    def filter_one_with_lazy(self, *criterion) -> Provide:
        query = self.db_session.query(self.cls).options(
            joinedload(Provide.service, innerjoin=True),
            joinedload(Provide.city, innerjoin=True)
        ).filter(*criterion)
        return query.one_or_none()
