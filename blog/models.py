from django.db import models

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=100)
    main_image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title