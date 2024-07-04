# educations/serializers.py

from rest_framework.serializers import ModelSerializer
from economia.models import Blank, Multiple, Tf

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