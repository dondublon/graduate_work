from sqlalchemy import select

from db_profiles import get_session
from models_profiles.user import User


class UserService:
    @classmethod
    def register(cls, id_, first_name, family_name, father_name, phone, email):
        with get_session() as session:
            new_user = User(id=id_, first_name=first_name, family_name=family_name,
                            father_name=father_name,
                            phone=phone,
                            email=email)
            session.add(new_user)
            session.commit()

    @classmethod
    def get_by_id(cls, id_) -> dict | None:
        # noinspection PyTypeChecker
        user_q = select(User).where(User.id == id_)
        with get_session() as session:
            user = session.scalar(user_q)
            if user:
                as_dict = user.as_dict(to_str=True)
                return as_dict
            else:
                return None

    @classmethod
    def change_email(cls, user_id, email):
        # noinspection PyTypeChecker
        user_q = select(User).where(User.id == user_id)
        with get_session() as session:
            user = session.scalar(user_q)
            user.email = email

            session.commit()

    @classmethod
    def update(cls, user_id, first_name, family_name, father_name, phone):
        # noinspection PyTypeChecker
        user_q = select(User).where(User.id == user_id)
        with get_session() as session:
            user = session.scalar(user_q)
            user.first_name = first_name
            user.family_name = family_name
            user.father_name = father_name
            user.phone = phone

            session.commit()

    @classmethod
    def get_users_profiles(cls, users_id: list) -> list:
        if users_id[0] == '*':
            profiles_q = select(User)
        else:
            profiles_q = select(User).filter(User.id.in_(users_id))
        with get_session() as session:
            profiles = session.scalars(profiles_q).all()
            if profiles:
                as_dict = [profile.as_dict(to_str=True) for profile in profiles]
                return as_dict
            else:
                return []
