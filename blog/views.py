from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import BlogSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Blog, Comment


class BlogsView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(
        tags=['blog'],
        description='List all active blogs',
        summary='List all active blogs',
        request=BlogSerializer,
        responses={200: BlogSerializer(many=True)}
    )
    def get(self, request):
        blogs = Blog.objects.filter(active=True)
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

    @extend_schema(
        tags=['blog'],
        description='Create a new blog',
        summary='Create a new blog',
        request=BlogSerializer,
        responses={201: BlogSerializer}
    )
    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(
        tags=['blog'],
        description='Retrieve a blog by id',
        summary='Retrieve a blog by id',
        responses={200: BlogSerializer}
    )
    def get(self, request, blog_id, *args, **kwargs):
        try:
            blog = Blog.objects.get(id=blog_id)
        except Blog.DoesNotExist:
            return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BlogSerializer(blog)
        return Response(serializer.data)

    @extend_schema(
        tags=['blog'],
        description='Update a blog by id',
        summary='Update a blog by id',
        request=BlogSerializer,
        responses={200: BlogSerializer}
    )
    def put(self, request, blog_id):

        try:
            # get blog by user and blog id
            blog = request.user.blogs.get(id=blog_id)
        except Blog.DoesNotExist:
            return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BlogSerializer(blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=['blog'],
        description='Delete a blog by id',
        summary='Delete a blog by id',
        responses={204: 'No content'}
    )
    def delete(self, request, blog_id):
        try:
            # get blog by user and blog id
            blog = request.user.blogs.get(id=blog_id)
        except Blog.DoesNotExist:
            return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)

        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BlogCommentView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @extend_schema(
        tags=['blog'],
        description='Create a comment for a blog',
        summary='Create a comment for a blog',
        request=CommentSerializer,
        responses={201: CommentSerializer},
        parameters=[
            OpenApiParameter(name='blog_id', type=int, location=OpenApiParameter.PATH, required=True)
        ]
    )
    def post(self, request, blog_id):
        try:
            blog = Blog.objects.get(id=blog_id)
        except Blog.DoesNotExist:
            return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, blog=blog)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(
        tags=['blog'],
        description='Update a comment for a blog',
        summary='Update a comment for a blog',
        request=None,
        responses={200: CommentSerializer},
        parameters=[
            OpenApiParameter(name='blog_id', type=int, location=OpenApiParameter.PATH, required=True),
            OpenApiParameter(name='comment_id', type=int, location=OpenApiParameter.QUERY, required=True),
            OpenApiParameter(name='content', type=str, location=OpenApiParameter.QUERY, required=True),
        ]
    )
    def put(self, request, blog_id):

        comment_id = request.data.get('comment_id')

        try:
            blog = Blog.objects.get(id=blog_id)
        except Blog.DoesNotExist:
            return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            comment = blog.comments.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(
        tags=['blog'],
        description='Delete a comment for a blog',
        summary='Delete a comment for a blog',
        responses={204: None},
        parameters=[
            OpenApiParameter(name='blog_id', type=int, location=OpenApiParameter.PATH, required=True),
            OpenApiParameter(name='comment_id', type=int, location=OpenApiParameter.QUERY, required=True),
        ]
    )
    def delete(self, request, blog_id):

        comment_id = request.data.get('comment_id')

        try:
            blog = Blog.objects.get(id=blog_id)
        except Blog.DoesNotExist:
            return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            comment = blog.comments.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)