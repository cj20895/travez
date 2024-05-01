from django.urls import path
from . import views
from .views import itinerary_list, add_itinerary, chatbot_response
app_name = 'itineraries'

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),


    # custom
    path('itineraries/', itinerary_list, name='itinerary_list'),
    path('itineraries/add/', add_itinerary, name='add_itinerary'),
    path('chatbot_response', views.chatbot_response, name='chatbot_response'),


]
