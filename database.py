from email.policy import default

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from datetime import datetime
import enum

Base = declarative_base()


class CatGender(enum.Enum):
    MALE = "Мужской"
    FEMALE = "Женский"


class CatWoll(enum.Enum):
    SMOOTH_HAIRED = 'Гладкошерстный'
    FLUFFY = "Пушистый"


# Определяем перечисление для ролей пользователей
class UserRole(enum.Enum):
    USER = "Пользователь"
    ADMIN = "Администратор"
    BANNED = "Заблокирован"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    username = Column(String(50))
    first_name = Column(String(50))
    last_name = Column(String(50))
    registration_date = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    email = Column(String(100), nullable=True)
    phone_number = Column(String(20), nullable=True)
    role = Column(Enum(UserRole), default=UserRole.USER)
    key_active = Column(Boolean, default=False)


    def __repr__(self):
        return f"<User(telegram_id={self.telegram_id}, username='{self.username}', role={self.role}, key_active={self.key_active})>"


class Cat(Base):
    __tablename__ = "cats"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    gender = Column(Enum(CatGender))
    age = Column(Integer)
    color = Column(String(50))
    wool = Column(Enum(CatWoll))
    cat_tray = Column(Boolean, default=False)
    parasite = Column(Boolean, default=False)
    vacine = Column(Boolean, default=False)
    chipped = Column(Boolean, default=False)
    sterilized = Column(Boolean, default=False)
    passport = Column(Boolean, default=False)
    cost = Column(Integer, default=0)

    def __repr__(self):
        return f"<Cat(name='{self.name}', gender={self.gender}, age={self.age})>"


engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


def get_session():
    """Создает и возвращает сессию базы данных."""
    return Session()


def create_user(telegram_id, username, first_name, last_name, email=None, phone_number=None, role=UserRole.USER,
                key_active=False):  # Изменение
    session = get_session()
    try:
        new_user = User(telegram_id=telegram_id, username=username, first_name=first_name, last_name=last_name,
                        email=email, phone_number=phone_number, role=role, key_active=key_active)  # Изменение
        session.add(new_user)
        session.commit()
        return new_user
    except Exception as e:
        session.rollback()
        print(f"Ошибка при создании пользователя: {e}")
        return None
    finally:
        session.close()


def get_user(telegram_id):
    session = get_session()
    try:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        return user
    finally:
        session.close()


def update_user_role(telegram_id, role: UserRole): #Удалили, status: UserStatus
    session = get_session()
    try:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if user:
            user.role = role
            session.commit()
            return True
        else:
            return False
    except Exception as e:
        session.rollback()
        print(f"Ошибка при обновлении роли пользователя: {e}")
        return False
    finally:
        session.close()

def get_user_by_username(username):
    session = get_session()
    try:
        user = session.query(User).filter_by(username=username).first()
        return user
    finally:
        session.close()

def create_cat(name, gender: CatGender, age, color: str, wool: CatWoll, cat_tray: bool, parasite: bool, vacine: bool,
               chipped: bool, sterilized: bool, passport: bool, cost: int):
    session = get_session()
    try:
        new_cat = Cat(name=name, gender=gender, age=age, color=color, wool=wool, cat_tray=cat_tray, parasite=parasite,
                      vacine=vacine, chipped=chipped,sterilized=sterilized, passport=passport,cost=cost)
        session.add(new_cat)
        session.commit()
        return new_cat
    except Exception as e:
        session.rollback()
        print(f"Ошибка при создании кота: {e}")
        return None
    finally:
        session.close()
