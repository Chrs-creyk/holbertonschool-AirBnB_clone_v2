#!/usr/bin/python3
"""This module defines a class to manage db storage for hbnb clone"""
import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import models

classes = {'User': User, 'Place': Place,
           'State': State, 'City': City, 'Amenity': Amenity,
           'Review': Review}


class DBStorage:
    """
    DBStorage class
    """
    __engine = None
    __session = None

    def __init__(self):
        ''' Init method for dbstorage'''
        user = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}:3306/{}".format(
            user, pwd, host, db), pool_pre_ping=True)
        metadata = MetaData()
        if os.getenv('HBNB_ENV') == 'test':
            metadata.drop_all()

    def all(self, cls=None):
        """
        Retrieves dictionary of objects in database
        Args:
            cls (obj): class of objects to be queried
        Returns:
            dictionary of objects
        """
        objs_dict = {}
        objs = None
        if cls:
            if type(cls) is str and cls in classes:
                cls = classes[cls]
            objs = self.__session.query(cls).all()
        else:
            objs = self.__session.query(User, State, City, Place).all()
        for obj in objs:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            objs_dict[key] = obj
        return (objs_dict)

    def new(self, obj):
        """
        Creates a query on current db session depending on class name
        """
        self.__session.add(obj)

    def save(self):
        """
        commit all changes of the current db session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        delete from current db session obj if not none
        """
        if obj:
            self.__session.delete(obj)
            self.save()

    def reload(self):
        """
        create all tb in db
        create current db session and is thread safe
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """
        Close session
        """
        self.__session.close()
