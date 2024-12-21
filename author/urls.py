from django.urls import path
from .views import (
    AuthorRegisterView,
    ResetPasswordSerializer, ResetPasswordView,
)

urlpatterns = [
    path("register/", AuthorRegisterView.as_view(), name="author"),
    path("change-password", ResetPasswordView.as_view(), name="author"),
]