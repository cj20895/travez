from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import os
from .models import Space, Review, Amenity, Tag  # Import necessary models
from datetime import datetime
from collections import defaultdict

# Assuming models.py is in the same directory or correctly referenced
# Initialize the engine (make sure to set your DATABASE_URL environment variable)
engine = create_engine(os.getenv('DATABASE_URL'))

def get_spaces():
    with Session(engine) as session:
        space_query = session.query(Space).filter(Space.approved == True)
        amenities_query = session.query(Amenity)
        spaces = [space.to_json() for space in space_query.all()]
        amenities = [amenity.to_json() for amenity in amenities_query.all()]

        # Organize amenities by space
        hm = defaultdict(list)
        for amenity in amenities:
            hm[amenity["spaceid"]].append(amenity["amenity"])

        for space in spaces:
            space.update({"amenities": hm[space["id"]]})

        data = {"spaces": spaces}
    return data

def get_space_by_name(name):
    with Session(engine) as session:
        space = session.query(Space).filter(Space.name == name).first()
        return space.to_json() if space else None

def get_space_details(space_id):
    with Session(engine) as session:
        space = session.query(Space).get(space_id)
        reviews = session.query(Review).filter(Review.space_id == space_id).all()
        amenities = session.query(Amenity).filter(Amenity.space_id == space_id).all()

        space_json = space.to_json()
        space_json['reviews'] = [review.to_json() for review in reviews]
        space_json['amenities'] = [amenity.to_json() for amenity in amenities]

        return space_json

def add_space(name, capacity, location, space_type, approved=True):
    with Session(engine) as session:
        new_space = Space(name=name, capacity=capacity, location=location, type=space_type, approved=approved)
        session.add(new_space)
        session.commit()
        return new_space.id

def update_space(space_id, **changes):
    with Session(engine) as session:
        space = session.query(Space).get(space_id)
        if space:
            for key, value in changes.items():
                setattr(space, key, value)
            session.commit()
            return f"Space with id '{space_id}' updated."
        else:
            return "Space not found."

def delete_space(space_id):
    with Session(engine) as session:
        space = session.query(Space).get(space_id)
        if space:
            session.delete(space)
            session.commit()
            return f"Deleted space with id {space_id}"
        else:
            return "Space not found."

def get_all_spaces():
    with Session(engine) as session:
        spaces = session.query(Space).all()
        return [space.to_json() for space in spaces]
    


# Note: Additional functions for handling reviews, tags, amenities should follow the same pattern.
# For simplicity, these CRUD operations have been outlined for the Space entity.
