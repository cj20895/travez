from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('space/<int:space_id>/', views.this_space, name='this_space'),  # To view and add reviews
    path('forum/', views.rankings_home, name='rankings_home'),  # Consider renaming for consistency
]
