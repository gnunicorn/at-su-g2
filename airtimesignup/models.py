from airtimesignup.database import Base
from sqlalchemy import (Column, Integer, ForeignKey, Unicode,
                        Sequence, Text, Float, DateTime, func)
from sqlalchemy.orm import relationship, backref


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    fullname = Column(Unicode)
    email = Column(Unicode)
    created = Column(DateTime, server_default=func.utc_timestamp())
    updated = Column(DateTime, server_default=func.utc_timestamp(),
                     onupdate=func.utc_timestamp())

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, Sequence('order_id_seq'), primary_key=True)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", backref=backref('orders', order_by=id))
    created = Column(DateTime, server_default=func.utc_timestamp())
    updated = Column(DateTime, server_default=func.utc_timestamp(),
                     onupdate=func.utc_timestamp())
    domain = Column(Unicode)
    state = Column(Unicode)
    address = Column(Text)
    vat_addr = Column(Unicode, nullable=True)
    currency = Column(Unicode)
    details = Column(Text)
    total = Column(Float(precision=2))
    total_vat = Column(Float(precision=2))
