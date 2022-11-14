import re
from uuid import uuid4
from dataclasses import dataclass
from sqlalchemy.orm import validates
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import check_password_hash, generate_password_hash

from app.configs.database import db
from app.exceptions.user_exceptions import EmailFormatError, NameFormatError


@dataclass
class User(db.Model):
    id: str
    name: str
    email: str

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(127), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    hash_password = Column(String(255))

    @property
    def password(self):
        raise AttributeError("Password cannot be accessed")

    @password.setter
    def password(self, password_to_hash):
        self.hash_password = generate_password_hash(password_to_hash)

    def check_password(self, password_to_compare):
        return check_password_hash(self.hash_password, password_to_compare)

    @validates("email")
    def verify_email(self, key, email_to_check: str):
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

        if re.fullmatch(regex, email_to_check):
            return email_to_check.lower()
        else:
            raise EmailFormatError

    @validates("name")
    def normalize_name(self, key, name_to_normalize: str):
        regex = r"^[a-zA-Z-0-9\s\w+]*$"

        if re.fullmatch(regex, name_to_normalize):
            return name_to_normalize.title()
        else:
            raise NameFormatError
