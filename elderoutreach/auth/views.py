from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

class AuthTest(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        user = request.user
        content = {"message": "yoyoyo", "logged_in_as": f"{user}"}
        return Response(content)

class APIChangePassword(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        user = request.user
        token = request.auth
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if password1 != password2:
            return Response({"error": "passwords do not match"})
        user.set_password(password1)
        user.save()
        return Response({"status": "success"})

# Create your views here.
