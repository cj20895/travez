from django.db import models
from django.contrib.auth.models import User

# If you want a custom user model, you'd need to create one before running migrations.

class Itinerary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='itinerary_images/')  # Image field

    # You can add other fields as necessary

    def __str__(self):
        return self.name
