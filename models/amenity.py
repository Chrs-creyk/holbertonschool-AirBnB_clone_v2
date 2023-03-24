#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import os
from os import getenv

env = getenv('HBNB_TYPE_STORAGE')


class Amenity(BaseModel, Base if os.getenv('HBNB_TYPE_STORAGE') == 'db' else object):
    """Amenity Class for HBnB"""
    if env == "db":
        __tablename__ = "amenities"
        name = Column(String(128), nullable=False)
    else:
        name = ""
