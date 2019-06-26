from typing import List, Tuple

from sqlalchemy.orm import joinedload

from infrastructure.repository import BaseRepository
from .model import Zone


class ZoneRepository(BaseRepository[Zone]):
    def __init__(self, **kwargs):
        super().__init__(Zone, **kwargs)

    def get_zone_list(self, query_string: str) -> Tuple[List[Zone], int]:
        return self.consume_search(query_string,
                                   opt=lambda x: x.options(joinedload(Zone.city, innerjoin=True)),
                                   opt2=lambda x: x)

    def filter_one_with_lazy(self, *criterion) -> Zone:
        query = self.db_session.query(self.cls).options(
            joinedload(Zone.city, innerjoin=True)
        ).filter(*criterion)
        return query.one_or_none()
