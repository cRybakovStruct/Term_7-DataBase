from sqlalchemy import Column, Integer, String, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Worker(Base):
    __tablename__ = 'workers'
    idworker = Column(Integer, primary_key=True)
    surname = Column(String)
    name = Column(String)
    fathername = Column(String)
    education = Column(String)
    town = Column(String)
    address = Column(String)
    phonenumber = Column(String)
    birthday = Column(Date)
    employ_date = Column(Date)
    salary = Column(Integer)
    position = Column(String)
    category = Column(Integer)
    unemploy_date = Column(Date)

    def __init__(self, surname, name, fathername, education, town, address, phonenumber, birthday, employ_date, salary, position, category, unemploy_date):
        # self.idworker = idworker
        self.surname = surname
        self.name = name
        self.fathername = fathername
        self.education = education
        self.town = town
        self.address = address
        self.phonenumber = phonenumber
        self.birthday = birthday
        self.employ_date = employ_date
        self.salary = salary
        self.position = position
        self.category = category
        self.unemploy_date = unemploy_date

    def __repr__(self):
        return "<Worker('%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')>" % (self.idworker, self.surname, self.name, self.fathername, self.education, self.town, self.address, self.phonenumber, self.birthday, self.employ_date, self.salary, self.position, self.category, self.unemploy_date)
    
class Fixation(Base):
    __tablename__ = 'fixations'
    # id = Column(Integer, primary_key=True)
    worker = Column(Integer, primary_key=True)
    shop = Column(String, primary_key=True)
    
    def __init__(self, worker, shop):
        self.worker = worker
        self.shop = shop

    def __repr__(self):
        return "<Fixation('%s','%s')>" % (self.worker, self.shop)