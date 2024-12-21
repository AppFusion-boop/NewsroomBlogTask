from django.contrib import admin
from django.db import models
from django.forms import SelectMultiple
from django.utils.safestring import mark_safe
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.forms.widgets import WysiwygWidget, ArrayWidget
from unfold.widgets import SelectMultiple
from .models import Blog, Category, Comment, MenuItem, BlogTag


class CommentInline(TabularInline):
    model = Comment
    extra = 0
    tab = True
    fields = ['author', 'content', 'likes', 'dislikes']
    readonly_fields = ['author', 'content', 'likes', 'dislikes']

    def has_add_permission(self, request, obj):
        return False


@admin.register(Blog)
class BlogAdmin(ModelAdmin):
    autocomplete_fields = ['author', 'tags']
    inlines = [CommentInline]
    list_display = ['title', 'author', 'active', 'created_at']
    search_fields = ['title']
    list_filter = ['active']
    fieldsets = (
        (None, {'fields': ('author', 'title', 'main_image', 'description', 'tags')}),
        ('Permissions', {'fields': ('active',)}),
    )
    ordering = ('title',)
    formfield_overrides = {
        models.TextField: {'widget': WysiwygWidget},
    }

def get_hierarchical_order(categories, parent=None, level=0):
    """
    Recursively generate a hierarchical order of categories.
    """
    result = []
    for category in categories.filter(parent=parent).order_by('name'):
        category.level = level  # Add a level attribute for later use
        result.append(category)
        result.extend(get_hierarchical_order(categories, parent=category, level=level + 1))
    return result


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['get_name', 'parent']
    search_fields = ['name']
    list_filter = ['parent']
    fieldsets = (
        (None, {'fields': ('name', 'parent')}),
    )
    # ordering = ('name',)
    formfield_overrides = {
        models.TextField: {'widget': WysiwygWidget},
        models.ManyToManyField: {'widget': ArrayWidget},
    }

    def get_name(self, obj):
        return mark_safe(f'{obj.get_depth() * '·&nbsp;&nbsp;&nbsp;&nbsp;'}{obj.name}')

    def get_queryset(self, request):
        """
        Override queryset to apply hierarchical ordering.
        """
        qs = super().get_queryset(request)
        ordered_categories = get_hierarchical_order(qs)
        # Preserve the ordering by IDs
        ordered_ids = [cat.id for cat in ordered_categories]
        return qs.filter(id__in=ordered_ids).order_by(
            models.Case(
                *[models.When(pk=pk, then=pos) for pos, pk in enumerate(ordered_ids)],
                default=models.Value(len(ordered_ids)),
                output_field=models.IntegerField(),
            )
        )


@admin.register(MenuItem)
class MenuItemAdmin(ModelAdmin):
    list_display = ['title', 'order', 'referring_category', 'link']
    search_fields = ['title', 'link']
    list_filter = ['referring_category']
    fieldsets = (
        (None, {'fields': ('title', 'order', 'referring_category', 'link')}),
    )
    ordering = ('order',)


@admin.register(BlogTag)
class BlogTagAdmin(ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    fieldsets = (
        (None, {'fields': ('name',)}),
    )
    ordering = ('name',)

