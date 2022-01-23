from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth import authenticate,logout
import requests
from pymongo import MongoClient
from django.contrib.auth import get_user_model

from authentication.api.serializers import ProfileSerializer, SignUPSerializer
from authentication.models import ProfileData
from student.models import StudentClasses

client = MongoClient('mongodb+srv://shashank:Shashank123@bigbuddy.g4rkw.mongodb.net/BigBuddy?retryWrites=true&w=majority')
userdb = client['BigBuddy']
UserModel = get_user_model()

class SignUPView(APIView):
    def post(self,request):
        serializer = SignUPSerializer(data=request.data)
        userData = {}
        if serializer.is_valid():
            userData['username'] = serializer.data['username']
            userData['email'] = serializer.data['email']
            userData['role'] = serializer.data['role']
            response = requests.post('http://127.0.0.1:8000/auth/profile/',data=userData)
            if response.status_code == 200:
                account = serializer.save()
                userData['Response'] = "Registration Successful"
                if userData['role'] == 'Student':
                    try:
                        studentClass = StudentClasses.objects.filter(email=userData['email'])
                    except StudentClasses.DoesNotExist:
                        pass
                    else:
                        studentData = {}
                        studentData['email'] = userData['email']
                        studentData['usercode'] = account.usercode
                        res = requests.put('http://127.0.0.1:8000/student/class/',data=studentData)
                        if res.status_code == 200:
                            response_2 = Response(userData)
                        else:
                            response_2 = Response(res)
            else:
                response_2 = Response(response)
            return response_2
        else:
            return Response(serializer.errors)
            
            
class ProfileView(APIView):
    def get(self, request):
        profile = ProfileData.objects.get(username=request.data.get('username'))
        serializer = ProfileSerializer(profile)
        return  Response(serializer.data)
    def post(self, request):
        requestedData = {}
        requestedData['username'] = request.data['username']
        requestedData['email'] = request.data['email']
        requestedData['role'] = request.data['role']
        
        serializer = ProfileSerializer(data=requestedData)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    def put(self, request):
        collection = userdb.get_collection('authentication_profiledata')
        profile = collection.find_one({'username': request.data.get('username')})
        serializer = ProfileSerializer(profile)
        data = {}
        data['username'] = serializer.data['username']
        data['email'] = serializer.data['email']
        data['role'] = serializer.data['role']
        if request.data.get('description'):
            data['description'] = request.data.get('description')
        if request.data.get('avatarURL'):
            data['avatarURL'] = request.data.get('avatarURL')
        serializer2 = ProfileSerializer(data=data)
        if serializer2.is_valid(): 
            collection.delete_one({'username': request.data.get('username')})  
            serializer2.save()
            return Response(serializer2.data)
        else:
            return Response(serializer2.errors)
        
class SignINView(APIView):
    def post(self, request):
        data = {}
        user = authenticate(username=request.data.get('username'),password=request.data.get('password'))
        if user is not None:
            refresh = RefreshToken.for_user(user)
            token = {
                                'refresh': str(refresh),
                                'access' : str(refresh.access_token)
                            }
            data['token'] = token
            data['Response'] = 'Login Successful'
            data['usercode'] = user.usercode
            response = Response(data)
            response.set_cookie('token',token)
            response.set_cookie('usercode',data['usercode'])
        else:
            data['Response'] = 'Credentials are not matching'
            response = Response(data)
        return response
        
            
            
class SignOUTView(APIView):
    def post(self, request):
        logout(request)
        response = Response("Logged out successfully",status=status.HTTP_200_OK)
        response.delete_cookie('token')
        response.delete_cookie('usercode')
        return response