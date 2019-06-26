from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer,
                        String)
from sqlalchemy.orm import relationship

from cities.model import City
from infrastructure.model import db


class Zone(db.Model):
    __tablename__ = 'zones'

    zone_id = Column(Integer, key='zone_id', primary_key=True, name='id')
    city_id = Column(ForeignKey(City.city_id))
    slug = Column(String(25), nullable=False,
                  comment='Alphanumeric url-valid string for natural accessing the item')
    title = Column(String(100), nullable=False, comment='Title of the zone')
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)
    is_active = Column(Boolean, nullable=False)
    city = relationship(City, innerjoin=True,
                        uselist=False, foreign_keys=[city_id])


@dataclass(frozen=True)
class ZoneDTO:
    zone_id: int = None
    city_id: int = None
    city_slug: str = None
    city_title: str = None
    slug: str = None
    title: str = None
    is_active: bool = False
    created_at: datetime = None
    updated_at: datetime = None
