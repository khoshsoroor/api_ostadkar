from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String
from sqlalchemy.orm import relationship

from infrastructure.model import db


class Skill(db.Model):

    __tablename__ = 'skills'

    skill_id = Column(Integer, key='skill_id', primary_key=True, name='id')
    slug = Column(String(25), nullable=False,
                  comment='Alphanumeric url-valid string for natural accessing the item')
    title = Column(String(100), nullable=False, comment='Title of the skill')
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)
    is_active = Column(Boolean, nullable=False)


@dataclass(frozen=True)
class SkillDTO:
    skill_id: int = None
    slug: str = None
    title: str = None
    is_active: bool = False
    created_at: datetime = None
    updated_at: datetime = None
