from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_utils import EmailType, PhoneNumberType
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, inspect


class Base(DeclarativeBase):
    def as_dict(obj, to_str=False):
        def getattr_here(attr_name):
            raw = getattr(obj, attr_name)
            return str(raw) if to_str else raw
        return {c.key: getattr_here(c.key)
                for c in inspect(obj).mapper.column_attrs}


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

    def __repr__(self):
        return f"<User {self.first_name} {self.family_name} <{self.email}>>"
