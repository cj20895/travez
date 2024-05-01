from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm, ItineraryForm
from .models import Itinerary
import os
from django.views.decorators.csrf import csrf_exempt
import requests
from django.views.decorators.http import require_http_methods
# from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import openai
from django.http import JsonResponse
from django.conf import settings
import json
from openai import OpenAI
client = OpenAI()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def itinerary_list(request):
    if request.user.is_authenticated:
        itineraries = Itinerary.objects.filter(user=request.user)
        return render(request, 'itineraries/itinerary_list.html', {'itineraries': itineraries})
    else:
        itineraries = Itinerary.objects.all()  # Get all itinerary objects
        return render(request, 'itineraries/itinerary_list.html', {'itineraries': itineraries})

def add_itinerary(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ItineraryForm(request.POST)
            if form.is_valid():
                itinerary = form.save(commit=False)
                itinerary.user = request.user
                itinerary.save()
                return redirect('itinerary_list')
        else:
            form = ItineraryForm()
        return render(request, 'itineraries/add_itinerary.html', {'form': form})
    else:
        return redirect('login')

@csrf_exempt
@require_http_methods(["POST"])
def chatbot_response(request):
    if request.method == 'POST':
            data = json.loads(request.body)
            user_message = data.get('message') # Make sure the key matches what's sent from the frontend

            # Process the message (placeholder for your chatbot logic)
            response_message = process_chat_message(user_message)
            
            return JsonResponse({'message': response_message})
        # except Exception as e:
    return JsonResponse({'error': 'Sorry, error encountered.'}, status=405)
    
def process_chat_message(message):
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",  # Ensure this model is correctly named and accessible
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}]
        )
        # Assuming the API response structure is parsed correctly below
        chat_response = response.choices[0].message.content  # Update path according to actual API response structure
        return chat_response
    except Exception as e:
        print(f"Error in process_chat_message: {e}")
        return "An error occurred while processing your message."
