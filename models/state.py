#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import Base
from models.base_model import BaseModel
from sqlalchemy.orm import relationship
import models
from models.city import City
import os
from sqlalchemy import Column, Integer, String, ForeignKey
from os import getenv

class State(BaseModel, Base if os.getenv('HBNB_TYPE_STORAGE') == 'db' else object):
    """ State class """
    __tablename__ = "states"
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state", cascade="all, delete")

    else:
        name = ''

        @property
        def cities(self):
            """Getter"""
            city_lst = []
            all_cities = models.storage.all(City)
            for city in all_cities.values():
                if city.state_id == self.id:
                    city_lst.append(city)
            return city_lst
