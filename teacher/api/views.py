from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
import json
import uuid
import datetime
import requests
from rest_framework import status

from teacher.api.serializers import ClassNotesSerializer, ClassRecordingSerializer, ClassRoomSerializer
from teacher.models import ClassNotes, ClassRecordings, ClassRoom

UserModel = get_user_model()

class ClassRoomListView(APIView):
    permission_classes =  [IsAuthenticated]
    def get(self,request):
        classRoom = ClassRoom.objects.filter(usercode=request.data.get('usercode'))
        serializer = ClassRoomSerializer(classRoom,many=True)
        return Response(serializer.data)
    def post(self,request):
        user = UserModel.objects.filter(username=request.user.username)
        if user.values('role')[0]['role']  == 'Teacher':
            data = {}
            studentData = {}
            data['className'] = request.data.get('className')
            data['teacherName'] = request.user.username
            data['classCode'] = str(uuid.uuid4())
            data['usercode'] = request.data.get('usercode')
            if request.data.get('videoStreamURL') :
                data['videoStreamURL'] = request.data.get('videoStreamURL')
            if request.data.get('classAvatarURL'):
                data['classAvatarURL'] = request.data.get('classAvatarURL')
            studentList =  request.data.get('studentList')
            data['studentList'] = studentList
            studentData['classCode'] = data['classCode']
            for email in request.data.get('studentList').split(','):
                studentData['email'] = email
                response = requests.post('http://api.bigbuddy.in/student/class/',data=studentData)
                if response.status_code == 201:
                    pass
                else:
                    return Response(response)
            serializer = ClassRoomSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response('You are not allowed to create a class')
    
class ClassRoomDetailView(APIView):
    permission_classes =  [IsAuthenticated]
    def get(self,request,className):
        classroomcode = self.request.headers['classCode']
        try:
            classRoom = ClassRoom.objects.filter(classCode = classroomcode)
        except:
            return Response('Classroom not Found!!',status=status.HTTP_400_NOT_FOUND)
        data={}
        data['className'] = classRoom.values('className')[0]['className']
        data['teacherName'] = classRoom.values('teacherName')[0]['teacherName']
        data['classCode'] = classRoom.values('classCode')[0]['classCode']
        data['usercode'] = classRoom.values('usercode')[0]['usercode']
        data['videoStreamURL'] = classRoom.values('videoStreamURL')[0]['videoStreamURL']
        data['classAvatarURL'] = classRoom.values('classAvatarURL')[0]['classAvatarURL']
        data['studentList'] = classRoom.values('studentList')[0]['studentList']
        serializer = ClassRoomSerializer(data)
        return Response(serializer.data)
    
    def put(self,request,className):
        classroomcode = request.data.get('classCode')
        try:
            classRoom = ClassRoom.objects.filter(classCode = classroomcode)
        except:
            return Response('Classroom not Found!!',status=status.HTTP_400_NOT_FOUND)
        if classRoom.values('usercode')[0]['usercode'] == request.data.get('usercode') and request.data.get('usercode') == request.user.usercode:
            data = {}
            if request.data.get('className'):
                data['className'] = request.data.get('className')
            else:
                data['className'] = classRoom.values('className')[0]['className']
            data['teacherName'] = request.user.username
            data['classCode'] = request.data.get('classCode')
            data['usercode'] = request.data.get('usercode')
            if request.data.get('videoStreamURL') :
                data['videoStreamURL'] = request.data.get('videoStreamURL')
            else:
                data['videoStreamURL'] = classRoom.values('videoStreamURL')[0]['videoStreamURL']
            if request.data.get('classAvatarURL'):
                data['classAvatarURL'] = request.data.get('classAvatarURL')
            else:
                data['classAvatarURL'] = classRoom.values('classAvatarURL')[0]['classAvatarURL']
            if request.data.get('studentList'):
                data['studentList'] = request.data.get('studentList')
            else:
                data['studentList'] = classRoom.values('studentList')[0]['studentList']
            classRoom.delete()
            serializer = ClassRoomSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,className):
        classroomcode = request.data.get('classCode')
        try:
            classRoom = ClassRoom.objects.get(classCode = classroomcode)
        except ClassRoom.DoesNotExist:
            return Response('Classroom not Found!!',status=status.HTTP_400_BAD_REQUEST)
        else:
            if classRoom.usercode == request.data.get('usercode') and request.data.get('usercode') == request.user.usercode:
                data={}
                data["classCode"] = classroomcode
                response = requests.delete('http://api.bigbuddy.in/student/class/',data=data)
                if response.status_code == 200:
                    pass
                else:
                    return Response(response)
                classRoom.delete()
                return Response('Class deleted successfully',status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        
class ClassNotesView(APIView):
    permission_classes =  [IsAuthenticated]
    def get(self, request,className):
        classroomcode = self.request.headers['classCode']
        try:
            classnotes = ClassNotes.objects.filter(classCode = classroomcode)
        except:
            return Response('No notes available for class')
        serializer = ClassNotesSerializer(classnotes, many=True)
        return Response(serializer.data)
    
    def post(self,request,className):
        classroomcode = request.data.get('classCode')
        usercode = request.data.get('usercode')
        dateandtime = datetime.datetime.now().ctime()
        noteslink = request.data.get('notes')
        data = {}
        data ['classCode'] = classroomcode
        data['usercode'] = usercode
        data['date'] = dateandtime
        data['noteslink'] = noteslink
        serializer = ClassNotesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
         
    def delete(self, request,className):
        classroomcode = request.data.get('classCode')
        noteslink = request.data.get('notes')
        if noteslink is None:
            return Response("Recording link is required")
        notes = ClassNotes.objects.filter(noteslink = noteslink)
        if request.data.get('usercode') == notes.values('usercode')[0]['usercode']:
            notes.delete()
            return Response("Notes deleted successfully",status=status.HTTP_200_OK)
        else: 
            return Response(status=status.HTTP_400_BAD_REQUEST)
            
class ClassRecordingView(APIView):
    permission_classes =  [IsAuthenticated]
    def get(self, request,className):
        classroomcode = self.request.headers['classCode']
        try:
            classrecordings = ClassRecordings.objects.filter(classCode = classroomcode)
        except:
            return Response('No recordings available for class')
        serializer = ClassRecordingSerializer(classrecordings, many=True)
        return Response(serializer.data)
    
    def post(self,request,className):
        classroomcode = request.data.get('classCode')
        usercode = request.data.get('usercode')
        dateandtime = datetime.datetime.now().ctime()
        recordinglink = request.data.get('recording')
        data = {}
        data['classCode'] = classroomcode
        data['usercode'] = usercode
        data['date'] = dateandtime
        data['recordinglink'] = recordinglink
        serializer = ClassRecordingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
         
    def delete(self, request,className):
        classroomcode = request.data.get('classCode')
        recordinglink = request.data.get('recording')
        if recordinglink is None:
            return Response("Recording link is required")
        recordings = ClassRecordings.objects.filter(recordinglink = recordinglink)
        if request.data.get('usercode') == recordings.values('usercode')[0]['usercode']:
            recordings.delete()
            return Response("Recordings deleted successfully",status=status.HTTP_200_OK)
        else: 
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        
    