from rest_framework import serializers
from economia.models import Player
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    player_id = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=255)



class CharacterSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    player_id = serializers.CharField(max_length=20)
    exp = serializers.CharField(max_length=255)

class ScenarioSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    player_id = serializers.CharField(max_length=20)
    exp = serializers.CharField(max_length=255)

class SubjectSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    subjects = serializers.CharField(max_length=20)
    chapters = serializers.CharField(max_length=1000)
    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Custom claims
        token['player_id'] = user.player_id
        token['player_name'] = user.player_name
        token['school'] = user.school
        token['nickname'] = user.nickname
        token['email'] = user.email

        return token

class UserLoginSerializer(serializers.Serializer):
    player_id = serializers.CharField(max_length=64, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        player_id = data.get("player_id")
        password = data.get("password")

        if Player.objects.filter(player_id=player_id).exists():
            user = Player.objects.get(player_id=player_id)
            if user.password == password:
                refresh = RefreshToken.for_user(user)
                access = CustomTokenObtainPairSerializer.get_token(user).access_token
                return {
                    'refresh': str(refresh),
                    'access': str(access)
                }
            else:
                raise serializers.ValidationError("Incorrect password")
        else:
            raise serializers.ValidationError("User does not exist")
        