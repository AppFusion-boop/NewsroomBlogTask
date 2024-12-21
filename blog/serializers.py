from rest_framework import serializers
from .models import Blog, Comment, BlogTag


class BlogTagSerializer(serializers.ModelSerializer):
    """Serializer for blog tags."""

    class Meta:
        model = BlogTag
        fields = ['id', 'name']


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comments with nested children."""
    author_name = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'blog', 'author', 'author_name', 'created_at', 'content', 'parent', 'children']
        read_only_fields = ['created_at', 'id', 'blog', 'author']

    def get_author_name(self, obj):
        return obj.author.username

    def get_children(self, obj):
        # Include nested children recursively
        children = obj.replies.all()
        if children.exists():
            return CommentSerializer(children, many=True, context=self.context).data
        return []


class BlogSerializer(serializers.ModelSerializer):
    """Serializer for blogs with nested tags and structured comments."""
    tags = BlogTagSerializer(many=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = ['id', 'title', 'main_image', 'description', 'created_at', 'tags', 'comments']
        read_only_fields = ['created_at', 'id']

    def get_comments(self, obj):
        # Include only root-level comments with nested structure
        root_comments = obj.comments.filter(parent=None)
        return CommentSerializer(root_comments, many=True, context=self.context).data

    def create(self, validated_data):
        # Handle tags while creating the blog
        tags_data = validated_data.pop('tags', [])
        blog = Blog.objects.create(**validated_data)

        # Create or get BlogTag instances and associate them with the blog
        tag_instances = [BlogTag.objects.get_or_create(name=tag['name'])[0] for tag in tags_data]
        blog.tags.set(tag_instances)

        return blog
