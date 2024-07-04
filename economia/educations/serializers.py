from rest_framework import serializers

class TFQuizSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    submitted_answer = serializers.CharField(max_length=1)
