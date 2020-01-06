from sqlalchemy import Column, Integer, String, Date, Boolean, Float, create_engine
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


class Machine(Base):
    __tablename__ = 'machines'
    model = Column(String, primary_key=True)
    eq_type = Column(String)
    length = Column(Float)
    width = Column(Float)
    height = Column(Float)
    weight = Column(Float)
    power = Column(Float)
    detail_length = Column(Float)
    detail_width = Column(Float)
    detail_thickness = Column(Float)
    tools = Column(String)
    manufacturer = Column(String)
    firm = Column(String)
    contact = Column(String)
    comments = Column(String)

    def __init__(self, model, eq_type, length, width, height, weight, power, detail_length, detail_width, detail_thickness, tools, manufacturer, firm, contact, comments):
        self.model = model
        self.eq_type = eq_type
        self.length = length
        self.width = width
        self.height = height
        self.weight = weight
        self.power = power
        self.detail_length = detail_length
        self.detail_width = detail_width
        self.detail_thickness = detail_thickness
        self.tools = tools
        self.manufacturer = manufacturer
        self.firm = firm
        self.contact = contact
        self.comments = comments

    def __repr__(self):
        return "<Machine('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (self.model, self.eq_type, self.length, self.width, self.height, self.weight, self.power, self.detail_length, self.detail_width, self.detail_thickness, self.tools, self.manufacturer, self.firm, self.contact, self.comments)


class Shop(Base):
    __tablename__ = 'shops'
    idshop = Column(String, primary_key=True)
    chief_IP = Column(String)
    chief_RP = Column(String)
    chief_DP = Column(String)
    chief_VP = Column(String)
    chief_TP = Column(String)
    chief_PP = Column(String)
    idshop_RP = Column(String)

    def __init__(self, idshop, chief_IP, chief_RP, chief_DP, chief_VP, chief_TP, chief_PP, idshop_RP):
        self.idshop = idshop
        self.chief_IP = chief_IP
        self.chief_RP = chief_RP
        self.chief_DP = chief_DP
        self.chief_VP = chief_VP
        self.chief_TP = chief_TP
        self.chief_PP = chief_PP
        self.idshop_RP = idshop_RP

    def __repr__(self):
        return "<Shop('%s','%s','%s','%s','%s','%s','%s','%s')" % (self.idshop, self.chief_IP, self.chief_RP, self.chief_DP, self.chief_VP, self.chief_TP, self.chief_PP, self.idshop_RP)


class Equipment(Base):
    __tablename__ = 'equipment'
    model = Column(String)
    creation_year = Column(Date)
    serial_number = Column(Integer, primary_key=True)
    placement = Column(String)
    start_using_date = Column(Date)
    comments = Column(String)

    def __init__(self, model, creation_year, serial_number, placement, start_using_date, comments):
        self.model = model
        self.creation_year = creation_year
        self.serial_number = serial_number
        self.placement = placement
        self.start_using_date = start_using_date
        self.comments = comments

    def __repr__(self):
        return "<Equipment('%s','%s','%s','%s','%s','%s')" % (self.model, self.creation_year, self.serial_number, self.placement, self.start_using_date, self.comments)


class Repair(Base):
    __tablename__ = 'repairs'
    idrepair = Column(Integer, primary_key=True)
    repair_name = Column(String)
    is_planned = Column(Boolean)
    receipt_date = Column(Date)
    start_date = Column(Date)
    finish_date = Column(Date)
    responsible_id = Column(Integer)
    equipment_id = Column(Integer)

    def __init__(self, repair_name, is_planned, receipt_date, start_date, finish_date, responsible_id, equipment_id):
        self.repair_name = repair_name
        self.is_planned = is_planned
        self.receipt_date = receipt_date
        self.start_date = start_date
        self.finish_date = finish_date
        self.responsible_id = responsible_id
        self.equipment_id = equipment_id

    def __repr__(self):
        return "<Repair('%s','%s','%s','%s','%s','%s','%s','%s')>" % (self.idrepair, self.repair_name, self.is_planned, self.receipt_date, self.start_date, self.finish_date, self.responsible_id, self.equipment_id)


class Fixation(Base):
    __tablename__ = 'fixations'
    worker = Column(Integer, primary_key=True)
    shop = Column(String, primary_key=True)

    def __init__(self, worker, shop):
        self.worker = worker
        self.shop = shop

    def __repr__(self):
        return "<Fixation('%s','%s')>" % (self.worker, self.shop)


class Performer(Base):
    __tablename__ = 'performers'
    repair_id = Column(Integer, primary_key=True)
    worker_id = Column(Integer, primary_key=True)

    def __init__(self, repair_id, worker_id):
        self.repair_id = repair_id
        self.worker_id = worker_id

    def __repr__(self):
        return "<Performer('%s','%s')" % (self.repair_id, self.worker_id)
