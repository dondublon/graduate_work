from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_utils import EmailType, PhoneNumberType
from werkzeug.security import generate_password_hash, check_password_hash

from db import db
# from models.mixins import ModelMixin


class User(db.Model):  # ModelMixin
    __tablename__ = "users"

    id = db.Column(  # no auto-fill
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False,
    )
    email = db.Column(EmailType, unique=True, nullable=True)
    first_name = db.Column(db.String, nullable=False)
    family_name = db.Column(db.String, nullable=False)
    father_name = db.Column(db.String, nullable=True)
    phone = db.Column(PhoneNumberType, unique=True, nullable=True)

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email: str) -> "User":
        return cls.query.filter_by(email=email).first()

    def __repr__(self):
        return f"<User {self.first_name} {self.family_name} <{self.email}>>"
