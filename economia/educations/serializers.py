# educations/serializers.py

from rest_framework.serializers import ModelSerializer
from economia.models import Blank, Multiple, Tf, Subjects, Stage

class BlankSerializer(ModelSerializer):
    class Meta:
        model = Blank
        fields = '__all__'
        
class MultipleSerializer(ModelSerializer):
    class Meta:
        model = Multiple
        fields = '__all__'
        
class TfSerializer(ModelSerializer):
    class Meta:
        model = Tf
        fields = '__all__'
        
class SubjectSerializer(ModelSerializer):
    class Meta:
        model = Subjects
        fields = '__all__'
        
class StageSerializer(ModelSerializer):
    class Meta:
        model = Stage
        fields = '__all__'
from rest_framework import serializers

class TFQuizSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    submitted_answer = serializers.CharField(max_length=1)
