from rest_framework.serializers import ModelSerializer
from economia.models import Scenario, Comments, ChildComments

class ScenarioSerializer(ModelSerializer):
    class Meta:
        model = Scenario
        fields = '__all__'
        
class CommentsSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'
        
class ChildCommentsSerializer(ModelSerializer):
    class Meta:
        model = ChildComments
        fields = '__all__'