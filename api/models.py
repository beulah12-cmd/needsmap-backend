from django.db import models
from django.contrib.auth.models import User

class NeedPost(models.Model):
    CATEGORY_CHOICES = [
        ('food', 'Food'),
        ('shelter', 'Shelter'),
        ('medical', 'Medical'),
        ('education', 'Education'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    location = models.CharField(max_length=200)  # We'll improve this later with GeoDjango
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_fulfilled = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

class Response(models.Model):
    need_post = models.ForeignKey(NeedPost, on_delete=models.CASCADE, related_name='responses')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Response to {self.need_post.title}"