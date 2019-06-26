from typing import List, Tuple

from infrastructure.repository import BaseRepository

from .model import Skill


class SkillRepository(BaseRepository[Skill]):
    def __init__(self, **kwargs):
        super().__init__(Skill, **kwargs)

    def get_skill_list(self,
                       query_string: str) -> Tuple[List[Skill], int]:

        return self.consume_search(query_string)
