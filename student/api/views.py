from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from student.api.serializers import StudentClassSerializer
from student.models import StudentClasses
from teacher.api.serializers import ClassRoomSerializer
from teacher.models import ClassRoom

UserModel = get_user_model()

class StudentClassesView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self,request):
        usercode = self.request.headers['usercode']
        data={}
        try:
            classroomcodes = StudentClasses.objects.filter(usercode = usercode)
        except:
            return Response("No classes yet!!")
        i=1
        for code in classroomcodes.values('classCode'):
            classroom = ClassRoom.objects.get(classCode = code["classCode"])
            serializer = ClassRoomSerializer(classroom)
            data['class '+str(i)] = serializer.data
            i+=1
        return Response(data)
    
    def post(self,request):
        data = {}
        data['email'] = request.data.get('email')
        data['classCode'] =  request.data.get('classCode')
        try:
            data['usercode'] = UserModel.objects.get(email=data['email']).usercode
        except UserModel.DoesNotExist:
            data['usercode'] = None
        serializer = StudentClassSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request):
        data = {}
        data['usercode'] = request.data.get('usercode')
        data['email'] =  request.data.get('email') 
        try:
            StudentClasses.objects.filter(email=data['email']).update(usercode=data['usercode'])
        except StudentClasses.DoesNotExist:
            return Response(status=status.HTTP_100_CONTINUE)
        else:
            return Response(status=status.HTTP_200_OK)
        
    def delete(self,request):
        classroomcode = request.data.get('classCode')
        if request.data.get('req'):
            req = request.data.get('req')
            if req == 'student':
                email = request.data.get('email')
                try:
                    student = StudentClasses.objects.filter(email = email).filter(classCode = classroomcode)
                except StudentClasses.DoesNotExist:
                    return Response("Student is not there in this class")
                else:
                    student.delete()
                    return Response('Deleted Successfully!!', status=status.HTTP_200_OK)
        else:
            if StudentClasses.objects.filter(classCode = classroomcode).delete():
                return Response('Deleted Successfully!!', status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)