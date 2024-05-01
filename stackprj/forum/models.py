
# Create your models here.
from sqlalchemy import Column, ForeignKey, String, Integer, Boolean, Float, create_engine
from sqlalchemy.orm import declarative_base, relationship, column_property
from sqlalchemy.sql import select, func
import uuid
import os

import collections

from guid import GUID


# -----------------------------------------------------------------------

Base = declarative_base()

# NEED TO EXPORT DATABASE URL

# export   DATABASE_URL=postgresql://fiosxuxc:SB_KyyR3331lTjt8SJZWJmunVk4cGk1i@kashin.db.elephantsql.com/fiosxuxc


# database_url = os.getenv('DATABASE_URL', 'postgresql://fiosxuxc:SB_KyyR3331lTjt8SJZWJmunVk4cGk1i@kashin.db.elephantsql.com/fiosxuxc')



class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    space_id = Column(Integer, ForeignKey('spaces.id', ondelete='CASCADE'))
    rating = Column(Integer)
    content = Column(String)
    cleanliness = Column(Integer)
    noisiness = Column(Integer)
    privacy = Column(Integer)
    lighting = Column(Integer)
    amenities_rating = Column(Integer)
    # Relationships
    space = relationship("Space", back_populates="reviews")
    tags = relationship("Tag", cascade="all,delete", back_populates="review")
    amenities = relationship("Amenity", cascade="all,delete", back_populates="review")
    def to_json(self):
        return {
            'id': self.id,
            'space_id': self.space_id,
            'rating': self.rating,
            'content': self.content,
            'cleanliness': self.cleanliness,
            'noisiness': self.noisiness,
            'privacy': self.privacy,
            'lighting': self.lighting,
            'amenities_rating': self.amenities_rating,
            'space': self.space.to_json() if self.space else None,
            'tags': [tag.to_json() for tag in self.tags],
            'amenities': [amenity.to_json() for amenity in self.amenities]
        }



class Space(Base):
    __tablename__ = 'spaces'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    location = Column(String)
    capacity = Column(Integer)
    numreviews = Column(Integer)
    rating = Column(Float, nullable=True)
    numvisits = Column(Integer)
    approved = Column(Boolean, default=True)
    avgcleanliness = Column(Float, nullable=True)
    avgnoise = Column(Float, nullable=True)
    avgprivacy = Column(Float, nullable=True)
    avglighting = Column(Float, nullable=True)
    avgamenities = Column(Float, nullable=True)
    # Relationships
    reviews = relationship("Review", cascade="all, delete", back_populates="space")
    amenities = relationship("Amenity", cascade="all,delete", back_populates="space")
    tags = relationship("Tag", cascade="all,delete", back_populates="space")
        
    # Calculate average rating using a column property
    # average_rating = column_property(select([func.coalesce(func.avg(Review.rating), 0)]).where(Review.space_id == id).correlate_except(Review))
    # average_rating = column_property(
    #     select([func.coalesce(func.avg(Review.rating), 0).label('average_rating')])
    #     .where(Review.space_id == id)
    #     .correlate_except(Review)
    #     .scalar_subquery()
    # )


    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "location": self.location,
            "capacity": self.capacity,
            "numreviews": self.numreviews,
            "rating": self.rating,
            "numvisits": self.numvisits,
            "approved": self.approved,
            "cleanliness": self.avgcleanliness,
            "noisiness": self.avgnoise,
            "privacy": self.avgprivacy,
            "lighting": self.avglighting,
            "amenities_rating": self.avgamenities,
            # "average_rating": self.average_rating,

        }


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    space_id = Column(Integer, ForeignKey('spaces.id', ondelete='CASCADE'))
    review_id = Column(Integer, ForeignKey('reviews.id', ondelete='CASCADE'))
    tag = Column(String)
    # Relationships
    space = relationship("Space", back_populates="tags")
    review = relationship("Review", back_populates="tags")

class Amenity(Base):
    __tablename__ = 'amenities'
    id = Column(Integer, primary_key=True)
    space_id = Column(Integer, ForeignKey('spaces.id', ondelete='CASCADE'))
    review_id = Column(Integer, ForeignKey('reviews.id', ondelete='CASCADE'))
    amenity = Column(String)
    # Relationships
    space = relationship("Space", back_populates="amenities")
    review = relationship("Review", back_populates="amenities")

# Connection setup
if __name__ == "__main__":
    engine = create_engine(os.getenv("DATABASE_URL"))
    Base.metadata.create_all(engine)  # Create tables if they don't exist
    engine.dispose()
