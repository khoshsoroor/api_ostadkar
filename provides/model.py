from dataclasses import dataclass
from datetime import datetime, time

from sqlalchemy import (Boolean, Column, ForeignKey, Integer)
from sqlalchemy.types import Time, DateTime
from sqlalchemy.dialects.postgresql import JSONB, ENUM
from sqlalchemy.orm import relationship

from cities.model import City
from enums import Gender
from infrastructure.model import db
from services.model import Service


class Provide(db.Model):
    __tablename__ = 'provides'
    __table_args__ = (
        db.UniqueConstraint('city_id', 'service_id', 'gender'),
    )

    provide_id = Column(Integer, key='provide_id', primary_key=True, name='id')

    city_id = Column(ForeignKey(City.city_id), nullable=True)
    service_id = Column(ForeignKey(Service.service_id), nullable=True)
    gender = Column(ENUM(Gender), nullable=False)

    start_at = Column(Time, nullable=False)
    finish_at = Column(Time, nullable=False)

    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)
    is_active = Column(Boolean, nullable=False)

    city = relationship(City, innerjoin=True, uselist=False, foreign_keys=[city_id])
    service = relationship(Service, innerjoin=True, uselist=False, foreign_keys=[service_id])


@dataclass(frozen=True)
class ProvideDTO:
    provide_id: int = None
    city_title: str = None
    city_slug: str = None
    service_title: str = None
    service_slug: str = None
    gender: Gender = None
    start_at: time = None
    finish_at: time = None
    is_active: bool = False
    created_at: datetime = None
    updated_at: datetime = None
