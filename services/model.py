from enum import Enum

from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.orm import relationship

from infrastructure.model import db
from datetime import datetime
from dataclasses import dataclass


class Service(db.Model):

    __tablename__ = 'services'

    service_id = Column(Integer, key='service_id', primary_key=True, name='id')
    slug = Column(String(25), nullable=False, comment='Alphanumeric url-valid string for natural accessing the item')
    title = Column(String(160), nullable=False, comment='Title of the service')
    created_at = Column(String, nullable=False)
    updated_at = Column(String)
    is_active = Column(Boolean, nullable=False)


@dataclass(frozen=True)
class ServiceDTO:
    service_id: int = None
    slug: str = None
    title: str = None
    is_active: bool = False
    created_at: datetime = None
    updated_at: datetime = None