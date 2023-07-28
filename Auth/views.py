from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status,viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
import jwt
from .serializers import UserSerializer

class ListUsers(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [permissions.IsAdminUser]
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({"msg":"Success","data":serializer.data,"status":status.HTTP_200_OK})

class Loginuser(APIView):
    def post(self, request, format=None):
       serializer = UserSerializer(data=request.data,many=False)
       print(serializer.is_valid(),request.data)
       if serializer.is_valid():
            user = User.objects.filter(email=serializer.validated_data['email']).first()
            if user is not None and user.check_password(request.data['password']):
                serializer.validated_data.pop('password')
                val = jwt.encode(serializer.validated_data, settings.SECRET_KEY, algorithm='HS256')
                print(val)
                return Response({"msg":"User Logged in Successfully","data":{"token":{val}},"status":status.HTTP_200_OK})
            else:
                return Response({"msg":"Invalid credentials","data":{"token":{}},"status":status.HTTP_200_OK})
       else:
        return Response({"msg":"Invalid credentials","data":{"token":{}},"status":status.HTTP_200_OK})

class Registeruser(APIView):
   def post(self, request, format=None):
       serializer = UserSerializer(data=request.data,many=False)
       print(serializer.error_messages,serializer,serializer.is_valid())
       if serializer.is_valid():
        password = serializer.validated_data['password']
        # serializer.validated_data.pop('password')
        # serializer.validated_data["password"]=serializer.__hash__(password)
        serializer.save()
        return Response({"msg":"User Registered Successfully","status":status.HTTP_200_OK})
       else:
        return Response({"msg":"Data is incorrect","status":status.HTTP_200_OK})


class Deleteuser(APIView):
   authentication_classes = [JWTAuthentication]
   permission_classes = [permissions.IsAdminUser]
   def get(self,request,format=None):
        user = User.objects.all()
        user.delete()
        return Response({"msg":"All users deleted","status":status.HTTP_200_OK})
   
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
         