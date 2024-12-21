from django.db import models

# Create your models here.
class Blog(models.Model):
    author = models.ForeignKey('author.Author', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    main_image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    tags = models.ManyToManyField('BlogTag', related_name='blogs')

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')

    def get_depth(self):
        """Calculate the depth dynamically."""
        depth = 0
        parent = self.parent
        while parent:
            depth += 1
            parent = parent.parent
        return depth

    def __str__(self):
        return f'{self.parent} > {self.name}' if self.parent else self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('author.Author', on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='replies')
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content


class BlogTag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    title = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)
    referring_category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    link = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Menu Items'
