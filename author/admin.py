from django.contrib import admin
from .models import Author
from blog.models import Blog
from unfold.admin import ModelAdmin, TabularInline
# Register your models here.


class BlogInline(TabularInline):
    model = Blog
    extra = 0
    tab = True
    fields = ['title', 'active']

    def has_add_permission(self, request, obj):
        return False


@admin.register(Author)
class AuthorAdmin(ModelAdmin):

    inlines = [BlogInline]

    list_display = ['username', 'email', 'is_active']
    search_fields = ['username', 'email']
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    ordering = ('username',)
