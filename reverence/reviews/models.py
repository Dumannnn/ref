from django.db import models
from django.utils import timezone

class Review(models.Model):
    author = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.author} ({self.rating}/5)"
