import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Space  # Ensure your models are correctly imported

# Define the sample data
new_york_landmarks = [
    {"name": "Statue of Liberty", "type": "Monument", "location": "New York Harbor", "capacity": 5000, "approved": True},
    {"name": "Grand Central Station", "type": "Transport Hub", "location": "89 E 42nd Street", "capacity": 75000, "approved": True},
    {"name": "Empire State Building", "type": "Skyscraper", "location": "350 5th Avenue", "capacity": 20000, "approved": True},
    {"name": "Central Park", "type": "Public Park", "location": "Central Park", "capacity": 250000, "approved": True},
    {"name": "Brooklyn Bridge", "type": "Bridge", "location": "East River", "capacity": 10000, "approved": True},
    {"name": "Times Square", "type": "Commercial Area", "location": "Manhattan, NY 10036", "capacity": 50000, "approved": True},
    {"name": "Rockefeller Center", "type": "Historic Building", "location": "45 Rockefeller Plaza", "capacity": 15000, "approved": True},
    {"name": "The Metropolitan Museum of Art", "type": "Museum", "location": "1000 5th Avenue", "capacity": 20000, "approved": True},
    {"name": "One World Trade Center", "type": "Skyscraper", "location": "285 Fulton St", "capacity": 25000, "approved": True},
    {"name": "High Line", "type": "Park", "location": "West Side, NY", "capacity": 10000, "approved": True}
]

# Connection setup
if __name__ == "__main__":
    engine = create_engine(os.getenv("DATABASE_URL"))
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Create all tables if they don't exist
    Base.metadata.create_all(engine)

    # Populate the database with New York City landmarks
    for landmark in new_york_landmarks:
        space = Space(**landmark)
        session.add(space)

    # Commit the session and print a success message
    session.commit()
    print("Database populated with New York City landmarks!")

    # Close the session and dispose of the engine
    session.close()
    engine.dispose()
