from ninja import Router, Schema, NinjaAPI, Field
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from ninja import NinjaAPI, Router, Schema, ModelSchema, Form
from typing import List, Optional
from api.models import *
from django.contrib.auth.hashers import make_password
from pydantic import field_validator
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, date
from ninja.responses import Response
from rest_framework import status


router = Router()


class UserSchema(Schema):
    username: str
    password: str
    password2: str
    first_name: str
    last_name : str
    birth_date: date
    phone_number: str
    email: str
    
    @field_validator("password2")
    def passwords_match(cls, password2, values, **kwargs):
        if "password" in values.data and values.data["password"] != password2:
            raise ValueError("Passwords do not match")
        return password2
    
class LoginSchema(Schema):
    username: str
    password: str

class LoginResponseSchema(Schema):
    username: str
    password: str
    access_token: str
    refresh_token: str
    

class UserResponseSchema(Schema):
    username: str


class UserAPI:
            
    @router.post('/register', response=UserResponseSchema)
    def create_user(request, form: UserSchema = Form(...)):
        if form.password != form.password2:
            return {"error": "Passwords do not match"}
        if AttendeeUser.objects.filter(username = form.username).exists():
            return {"error": "Username already taken"}
        user = AttendeeUser.objects.create(username = form.username, password =make_password(form.password), birth_date = form.birth_date, 
                                           phone_number = form.phone_number, email = form.email, first_name = form.first_name, last_name = form.last_name)
        return {"username":user.username}
    
    
    
    @router.post('/login', response = LoginResponseSchema)
    def login(request, form: LoginSchema = Form(...)):
        user = authenticate(request, username = form.username, password = form.password)
            
        if user is not None:
            login(request,user)
            refresh = RefreshToken.for_user(user)
            return {
                "success": True,
                "message": "Login successful",
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
                "username": user.username,
                "password": user.password,
            }
        else:
            return Response(
            {"success": False, "message": "Invalid username or password"},
            status=status.HTTP_403_FORBIDDEN
        )
        
    @router.get('/profile', response=UserResponseSchema)
    def view_profile(request):
        """
        Retrieve the profile details of the currently logged-in user.

        Returns:
            The user's profile information including username and tokens.
        """
        user = request.user
        if not user.is_authenticated:
            return Response(
                {"error": "User is not authenticated"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        refresh = RefreshToken.for_user(user)
        return {
            "username": user.username,
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        }
