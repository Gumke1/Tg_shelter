from sqlalchemy import inspect
from sqlalchemy import select
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from datetime import datetime
import enum

# Создание базового класса для декларативных моделей
Base = declarative_base()

# Перечисление для пола кота
class CatGender(enum.Enum):
    MALE = "Мужской"
    FEMALE = "Женский"

# Перечисление для типа шерсти кота
class CatWoll(enum.Enum):
    SMOOTH_HAIRED = 'Гладкошерстный'
    FLUFFY = "Пушистый"

# Перечисление для ролей пользователей
class UserRole(enum.Enum):
    USER = "Пользователь"
    ADMIN = "Администратор"
    BANNED = "Заблокирован"

# Модель пользователя
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

# Модель кота
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
    photo_url = Column(String(100))
    identifier = Column(String(50), nullable=True, unique=True)  # Уникальный идентификатор кота
    description = Column(String(200), nullable=True)

    def __repr__(self):
        return f"<Cat(name='{self.name}', gender={self.gender}, age={self.age})>"

# Перечисление для типа заявки
class ApplicationType(enum.Enum):
    TAKE = "take"
    VOLUNTEER = "volunteer"

# Модель заявки
class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)  # ID пользователя в Telegram
    cat_identifier = Column(String)
    application_type = Column(Enum(ApplicationType))
    application_date = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Application(user_id={self.user_id}, cat_identifier={self.cat_identifier}, application_type={self.application_type})>"

# Создание движка базы данных
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

# Создание сессии
Session = sessionmaker(bind=engine)

# Проверка существования таблиц и их создание, если они отсутствуют
inspector = inspect(engine)
with engine.begin() as connection:
    if not inspector.has_table("users"):
        User.__table__.create(connection)
        print("Таблица 'users' создана.")
    if not inspector.has_table("cats"):
        Cat.__table__.create(connection)
        print("Таблица 'cats' создана.")
    if not inspector.has_table("applications"):
        Application.__table__.create(connection)
        print("Таблица 'applications' создана.")

# Функция для получения сессии базы данных
def get_session():
    """Создает и возвращает сессию базы данных."""
    return Session()

# Функция для создания пользователя
def create_user(telegram_id, username, first_name, last_name, email=None, phone_number=None, role=UserRole.ADMIN,
                key_active=False):
    session = get_session()
    try:
        new_user = User(telegram_id=telegram_id, username=username, first_name=first_name, last_name=last_name,
                        email=email, phone_number=phone_number, role=role, key_active=key_active)
        session.add(new_user)
        session.commit()
        return new_user
    except Exception as e:
        session.rollback()
        print(f"Ошибка при создании пользователя: {e}")
        return None
    finally:
        session.close()

# Функция для получения пользователя по telegram_id
def get_user(telegram_id):
    session = get_session()
    try:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        return user
    finally:
        session.close()

# Функция для обновления роли пользователя
def update_user_role(telegram_id, role: UserRole):
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

# Функция для получения пользователя по username
def get_user_by_username(username):
    session = get_session()
    try:
        user = session.query(User).filter_by(username=username).first()
        return user
    finally:
        session.close()

# Функция для получения кота по идентификатору
def get_cat_by_identifier(identifier):
    session = get_session()
    try:
        cat = session.query(Cat).filter_by(identifier=identifier).first()
        return cat
    finally:
        session.close()

# Функция для обновления данных кота
def update_cat(cat_id, name, gender, color, wool, cat_tray, parasite, vacine, chipped, sterilized, passport, cost,
               description):
    session = get_session()
    try:
        cat = session.query(Cat).filter_by(id=cat_id).first()
        if cat:
            # Обновление полей, если предоставлены новые значения
            if name is not None:
                cat.name = name
            if gender is not None:
                cat.gender = gender
            if color is not None:
                cat.color = color
            if wool is not None:
                cat.wool = wool
            if cat_tray is not None:
                cat.cat_tray = cat_tray
            if parasite is not None:
                cat.parasite = parasite
            if vacine is not None:
                cat.vacine = vacine
            if chipped is not None:
                cat.chipped = chipped
            if sterilized is not None:
                cat.sterilized = sterilized
            if passport is not None:
                cat.passport = passport
            if cost is not None:
                cat.cost = cost
            if description is not None:
                cat.description = description

            session.commit()
            return True
        else:
            return False  # Кот не найден
    except Exception as e:
        session.rollback()
        print(f"Ошибка при изменении данных кота: {e}")
        return False
    finally:
        session.close()

# Функция для удаления кота
def delete_cat(cat_id):
    session = get_session()
    try:
        cat = session.query(Cat).filter_by(id=cat_id).first()
        if cat:
            session.delete(cat)
            session.commit()
            return True
        else:
            return False  # Кот не найден
    except Exception as e:
        session.rollback()
        print(f"Ошибка при удалении кота: {e}")
        return False
    finally:
        session.close()

# Функция для получения всех ID котов
def get_all_cat_ids():
    """Получает список ID котов из базы данных."""
    session = get_session()
    try:
        # Запрос к базе данных через SQLAlchemy
        query = select(Cat.id)
        result = session.execute(query)

        cat_ids = [row[0] for row in result.all()]  # Извлечение всех ID котов

        return cat_ids
    except Exception as e:
        print(f"Ошибка при получении ID котов: {e}")
        return []
    finally:
        session.close()

# Функция для получения кота по ID
def get_cat(cat_id):
    session = get_session()
    try:
        cat = session.query(Cat).filter_by(id=cat_id).first()  # Поиск по ID
        return cat
    finally:
        session.close()

# Функция для поиска котов по заданным критериям
def find_cats(**kwargs):
    """Ищет котов на основе указанных критериев."""
    session = get_session()
    try:
        query = session.query(Cat)

        for key, value in kwargs.items():
            if value is not None:
                if key == "name":
                    query = query.filter(Cat.name.ilike(f"%{value}%"))  # Поиск без учета регистра
                elif key == "gender":
                    query = query.filter(Cat.gender == value)
                elif key == "age":
                    query = query.filter(Cat.age == value)
                elif key == "color":
                    query = query.filter(Cat.color.ilike(f"%{value}%"))
                elif key == "wool":
                    query = query.filter(Cat.wool == value)
                elif key == "cat_tray":
                    query = query.filter(Cat.cat_tray == value)
                elif key == "parasite":
                    query = query.filter(Cat.parasite == value)
                elif key == "vacine":
                    query = query.filter(Cat.vacine == value)
                elif key == "chipped":
                    query = query.filter(Cat.chipped == value)
                elif key == "sterilized":
                    query = query.filter(Cat.sterilized == value)
                elif key == "passport":
                    query = query.filter(Cat.passport == value)
                elif key == "cost":
                    query = query.filter(Cat.cost <= int(value))
                elif key == "description":
                    query = query.filter(Cat.description.ilike(f"%{value}%"))

        cats = query.all()

        return cats
    except Exception as e:
        print(f"Ошибка при поиске котов: {e}")
        return []
    finally:
        session.close()

# Функция для создания кота
def create_cat(name, gender: CatGender, age, color: str, wool: CatWoll, cat_tray: bool, parasite: bool, vacine: bool,
               chipped: bool, sterilized: bool, passport: bool, cost: int, photo_url: str, identifier: str,
               description: str) -> Cat:
    session = get_session()
    try:
        new_cat = Cat(name=name, gender=gender, age=age, color=color, wool=wool, cat_tray=cat_tray, parasite=parasite,
                      vacine=vacine, chipped=chipped, sterilized=sterilized, passport=passport, cost=cost,
                      photo_url=photo_url, identifier=identifier, description=description)
        session.add(new_cat)
        session.commit()
        return new_cat
    except Exception as e:
        session.rollback()
        print(f"Ошибка при создании кота: {e}")
        return None
    finally:
        session.close()

# Функция для создания заявки
def create_application(user_id, cat_identifier, application_type: ApplicationType):
    session = get_session()
    try:
        new_application = Application(user_id=user_id, cat_identifier=cat_identifier, application_type=application_type)
        session.add(new_application)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print(f"Ошибка при создании заявки: {e}")
        return False
    finally:
        session.close()

# Функция для получения всех заявок на взятие кота
def get_take_applications():
    """Получает все заявки на взятие кота из базы данных."""
    session = get_session()
    try:
        # Формирование запроса с использованием функции select SQLAlchemy
        query = select(Application).filter(Application.application_type == ApplicationType.TAKE)
        # Выполнение запроса
        result = session.execute(query)
        # Извлечение объектов Application из результата
        applications = result.scalars().all()
        return applications
    except Exception as e:
        print(f"Ошибка при получении заявок: {e}")
        return []
    finally:
        session.close()