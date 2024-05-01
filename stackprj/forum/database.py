from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import os
from .models import Space, Review, Amenity, Tag  # Import necessary models
from datetime import datetime
from collections import defaultdict

engine = create_engine(os.getenv('DATABASE_URL'))

def update_average_rating(space_id):
    with Session(engine) as session:
        ratings = session.query(Review.rating).filter(Review.space_id == space_id).all()
        if ratings:
            average = sum(rate[0] for rate in ratings) / len(ratings)
        else:
            average = 0
        space = session.query(Space).get(space_id)
        space.average_rating = average
        session.commit()

def add_review(space_id, rating, content):
    with Session(engine) as session:
        new_review = Review(space_id=space_id, rating=rating, content=content)
        session.add(new_review)
        session.commit()
    update_average_rating(space_id)  # Update average rating after adding the review

def get_spaces():
    with Session(engine) as session:
        space_query = session.query(Space).filter(Space.approved == True)
        amenities_query = session.query(Amenity)
        spaces = [space.to_json() for space in space_query.all()]
        amenities = [amenity.to_json() for amenity in amenities_query.all()]

        hm = defaultdict(list)
        for amenity in amenities:
            hm[amenity["spaceid"]].append(amenity["amenity"])

        for space in spaces:
            space.update({"amenities": hm[space["id"]]})

        return {"spaces": spaces}

def get_space_by_name(name):
    with Session(engine) as session:
        space = session.query(Space).filter(Space.name == name).first()
        return space.to_json() if space else None

# def get_space_details(space_id):
#     with Session(engine) as session:
#         space = session.query(Space).get(space_id)
#         reviews = session.query(Review).filter(Review.space_id == space_id).all()
#         amenities = session.query(Amenity).filter(Amenity.space_id == space_id).all()

#         space_json = space.to_json()
#         space_json['reviews'] = [review.to_json() for review in reviews]
#         space_json['amenities'] = [amenity.to_json() for amenity in amenities]

#         return space_json
def get_space_details(space_id):
    with Session(engine) as session:
        space = session.query(Space).get(space_id)
        if not space:
            return None  # Return None or an appropriate response if space not found

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
        update_average_rating(new_space.id)  # Initialize average rating
        return new_space.id

def update_space(space_id, **changes):
    with Session(engine) as session:
        space = session.query(Space).get(space_id)
        if space:
            for key, value in changes.items():
                setattr(space, key, value)
            session.commit()
            update_average_rating(space_id)  # Update average rating if changes might affect it
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
