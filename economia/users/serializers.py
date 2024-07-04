from rest_framework.serializers import ModelSerializer
from economia.models import Subjects, SubjectsScore, Characters, Player

class PlayerSerializer(ModelSerializer):
    class Meta:
        model = Player
        fields = ['nickname', 'school']

class CharactersSerializer(ModelSerializer):
    player = PlayerSerializer()

    class Meta:
        model = Characters
        fields = ['player']

class SubjectsSerializer(ModelSerializer):
    class Meta:
        model= Subjects
        fields = '__all__'
        
class SubjectsScoreSerializer(ModelSerializer):
    characters = CharactersSerializer()  
    
    class Meta:
        model= SubjectsScore
        fields = '__all__'