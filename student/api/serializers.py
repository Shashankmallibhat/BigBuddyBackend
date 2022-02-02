from rest_framework import serializers

from student.models import StudentClasses, StudentWishlist

class StudentClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentClasses
        fields = '__all__'
        
class StudentWishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentWishlist
        fields = '__all__'
        
