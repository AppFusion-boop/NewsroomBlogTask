from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import AuthorSerializer, RegisterSerializer, ResetPasswordSerializer


class AuthorRegisterView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = []
    serializer_class = AuthorSerializer

    @extend_schema(
        tags=["author"],
        responses=AuthorSerializer,
        request=RegisterSerializer,
        summary="Create a new author"
    )
    def post(self, request, *args, **kwargs):

        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return without password
            return Response(AuthorSerializer(serializer.instance).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ResetPasswordSerializer

    @extend_schema(
        tags=["author"],
        responses=ResetPasswordSerializer,
        summary="Change password"
    )
    def put(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(AuthorSerializer(serializer.instance).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
