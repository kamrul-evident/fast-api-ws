from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates
from datetime import datetime
import uuid
from slugify import slugify

# Create a declarative base class
Base = declarative_base()

# Define the abstract base class
class BaseModeWithUUID(Base):
    __tablename__ = "base_model"
    __abstract__ = True
    id = Column(Integer, primary_key=True, db_index=True)
    uid = Column(String, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    @validates("updated_at")
    def update_timestamp(self, key, value):
        return datetime.now()


class NameSlugDescriptionBaseModel(BaseModeWithUUID):
    __abstract__ = True
    name = Column(String, nullable=False)
    slug = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)

    @validates("name")
    def validate_name(self, key, name):
        assert name is not None
        return name

    @validates("slug")
    def validate_slug(self, key, slug):
        assert slug is not None
        return slug

    @validates("description")
    def validate_description(self, key, description):
        # Allow description to be optional, no assert needed
        return description

    # Using the `@validates` method to generate the slug automatically
    @validates("name")
    def generate_slug_from_name(self, key, name):
        # Slug is generated only if name is provided
        if name:
            self.slug = slugify(name)
        return name
