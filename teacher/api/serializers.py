from rest_framework import serializers

from teacher.models import ClassRecordings, ClassRoom,ClassNotes


class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = '__all__'

class ClassNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassNotes
        fields = '__all__'

class ClassRecordingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRecordings
        fields = '__all__'
        