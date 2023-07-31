from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
import datetime
import bcrypt
from zoneinfo import ZoneInfo
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status,viewsets
from cryptography.fernet import Fernet
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from passlib.hash import pbkdf2_sha256
import math
from .serializers import UserSerializer

class ListUsers(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({"msg":"Success","data":serializer.data,"status":status.HTTP_200_OK})

class Loginuser(APIView):
    def post(self, request, format=None):
       serializer = UserSerializer(data=request.data,many=False)
       email = request.data['email']
       psw = request.data['password']
       user = User.objects.filter(email=email).first()
       print("hello",user.pk,verify_password(user.password,psw),psw,user.password)
       if user is not None and verify_password(user.password,psw):
            refresh = RefreshToken.for_user(user)
            print(refresh)
            return Response({"msg":"User Logged in Successfully","data":{'refresh': str(refresh),
            'access': str(refresh.access_token)},"status":status.HTTP_200_OK})
            # return Response({"msg":"hello"})
       else:
        return Response({"msg":"Invalid credentials","data":{"token":{}},"status":status.HTTP_200_OK})

class Registeruser(APIView):
   def post(self, request, format=None):
    print("Gookss",request.data)
    serializer = UserSerializer(data=request.data,many=False)
    print(serializer.error_messages,serializer,serializer.is_valid())
    if serializer.is_valid():
        serializer.save()
        return Response({"msg":"User Registered Successfully","status":status.HTTP_200_OK})
    else:
        return Response({"msg":"Data is incorrect","status":status.HTTP_200_OK})


class Deleteuser(APIView):
   authentication_classes = [JWTAuthentication]
   permission_classes = [permissions.IsAuthenticated,permissions.IsAdminUser]
   def get(self,request,format=None):
        user = User.objects.all()
        user.delete()
        return Response({"msg":"All users deleted","status":status.HTTP_200_OK})
   
   authentication_classes = [JWTAuthentication]
   permission_classes = [permissions.IsAuthenticated]
   def post(self,request,format=None):
         serializer = UserSerializer(data=request.data,many=False)
         if serializer.is_valid():
              user = User.objects.filter(email=serializer.validated_data['email']).first()
              if user is not None and user.check_password(serializer.validated_data['password']):
                user.delete()
                return Response({"msg":"User deleted successfully","status":status.HTTP_200_OK})
              else:
                return Response({"msg":"Invalid credentials","status":status.HTTP_200_OK})
         else:
              return Response({"msg":"Invalid credentials","status":status.HTTP_200_OK})



def encrypt_password(pswd):
    bytes = pswd.encode()
    salt = bcrypt.gensalt(rounds=12)
    hash = bcrypt.hashpw(bytes, salt)
    return hash

def verify_password(pswd, e_pswd):
    # userBytes = e_pswd.encode('utf-8')
    # user = encrypt_password(e_pswd)
    # result = bcrypt.checkpw(pswd, e_pswd)
    return pswd==e_pswd
         