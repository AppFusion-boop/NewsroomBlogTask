from django.urls import path


from .views import BlogsView, BlogView, BlogCommentView

urlpatterns = [
    path('blogs/', BlogsView.as_view(), name='blog-list'),
    path('blogs/<int:blog_id>/', BlogView.as_view(), name='blog-detail'),
    path('blogs/<int:blog_id>/comments/', BlogCommentView.as_view(), name='blog-comments'),
]