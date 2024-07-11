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
        
        
from rest_framework import serializers
from rest_framework import validators  # Import validators
from economia.models import Characters, Player

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characters
        fields = '__all__'

# 캐릭터 생성
class CreateCharacterSerializer(serializers.ModelSerializer):
    player_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Characters
        fields = ['player_id', 'exp', 'last_quiz', 'kind', 'kind_url', 'score']

    def validate_player_id(self, value):
        try:
            player = Player.objects.get(pk=value)
        except Player.DoesNotExist:
            raise serializers.ValidationError("Player matching query does not exist.")
        return value

    def create(self, validated_data):
        player_id = validated_data.pop('player_id')
        player = Player.objects.get(pk=player_id)
        character = Characters.objects.create(player=player, **validated_data)
        return character

