from django.shortcuts import render
from django.db.models import Avg
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from django.shortcuts import render
from .database import get_spaces, get_space_details # Import get_spaces function from your database relevant file
# from .models import Activity
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .database import get_space_details, get_spaces  # Assuming these functions are well-defined

import os
from .models import Space, Review  # Ensure Review is correctly imported
from datetime import datetime


# Create your views here.
engine = create_engine(os.getenv('DATABASE_URL'))


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def this_space(request, space_id):
    if request.method == 'POST':
        return add_review(request, space_id)
    else:
        space_data = get_space_details(space_id)  # Fetch the space details
        return render(request, 'forum/this_space.html', {'space': space_data})

def add_review(request, space_id):
    if request.method == 'POST':
        overall_rating = request.POST.get('overall_rating')
        cleanliness = request.POST.get('cleanliness')
        noisiness = request.POST.get('noisiness')
        lighting = request.POST.get('lighting')
        privacy = request.POST.get('privacy')
        amenities_rating = request.POST.get('amenities_rating')
        content = request.POST.get('content')

        with Session(engine) as session:
            new_review = Review(
                space_id=space_id,
                rating=overall_rating,
                cleanliness=cleanliness,
                noisiness=noisiness,
                lighting=lighting,
                privacy=privacy,
                amenities_rating=amenities_rating,
                content=content
            )
            session.add(new_review)
            session.commit()

        return redirect('forum:this_space', space_id=space_id)
    else:
        return HttpResponse("Invalid request", status=400)


def rankings_home(request):
    spaces_data = get_spaces()  # Retrieve spaces from the database
    return render(request, 'forum/rankings_home.html', {'activities': spaces_data['spaces']})