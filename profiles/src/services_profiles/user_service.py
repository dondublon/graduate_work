from sqlalchemy import select, delete

from db_profiles import Session
from models_profiles.user import User
from logger import logger


class UserService:
    @classmethod
    @classmethod
    async def register(cls, id_, first_name, family_name, father_name, phone, email):
        async with Session() as session:
            async with session.begin():
                new_user = User(id=id_, first_name=first_name, family_name=family_name,
                                father_name=father_name,
                                phone=phone,
                                email=email)
                session.add(new_user)
                await session.commit()

    @classmethod
    async def get_by_id(cls, id_) -> dict | None:
        # noinspection PyTypeChecker
        user_q = select(User).where(User.id == id_)
        async with Session() as session:
            async with session.begin():
                user = await session.scalar(user_q)
                if user:
                    as_dict = user.as_dict(to_str=True)
                    return as_dict
                else:
                    return None

    @classmethod
    async def change_email(cls, user_id, email):
        # noinspection PyTypeChecker
        user_q = select(User).where(User.id == user_id)
        async with Session() as session:
            async with session.begin():
                user = await session.scalar(user_q)
                user.email = email

                await session.commit()

    @classmethod
    async def update(cls, user_id, first_name, family_name, father_name, phone):
        # noinspection PyTypeChecker
        user_q = select(User).where(User.id == user_id)
        async with Session() as session:
            async with session.begin():
                user = await session.scalar(user_q)
                user.first_name = first_name
                user.family_name = family_name
                user.father_name = father_name
                user.phone = phone

                await session.commit()

    @classmethod
    async def get_users_profiles(cls, users_id: list) -> list:
        if users_id[0] == '*':
            profiles_q = select(User)
        else:
            profiles_q = select(User).filter(User.id.in_(users_id))
        async with Session() as session:
            async with session.begin():
                profiles = await session.scalars(profiles_q).all()
                if profiles:
                    as_dict = [profile.as_dict(to_str=True) for profile in profiles]
                    return as_dict
                else:
                    return []

    @classmethod
    async def delete_profile(cls, user_id: str):
        user_q = delete(User).where(User.id == user_id)
        async with Session() as session:
            async with session.begin():
                result = await session.execute(user_q)
                logger.info("Deleting result %s", result)
                await session.commit()
