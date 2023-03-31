from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_utils import EmailType, PhoneNumberType
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy import String

# from werkzeug.security import generate_password_hash, check_password_hash

# from db import db
# from models.mixins import ModelMixin
class Base(DeclarativeBase):
    pass

class User(Base):  # ModelMixin
    __tablename__ = "users"

    id = mapped_column(  # no auto-fill
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False,
    )
    email = mapped_column(EmailType, unique=True, nullable=True)
    first_name = mapped_column(String(100), nullable=False)
    family_name = mapped_column(String(100), nullable=False)
    father_name = mapped_column(String(100), nullable=True)
    phone = mapped_column(PhoneNumberType, unique=True, nullable=True)

    # def save(self) -> None:
    #     db.session.add(self)
    #     db.session.commit()

    # @classmethod
    # def find_by_email(cls, email: str) -> "User":
    #     return cls.query.filter_by(email=email).first()

    def __repr__(self):
        return f"<User {self.first_name} {self.family_name} <{self.email}>>"
