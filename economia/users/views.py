import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from economia.models import Characters
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from .serializers import CreateCharacterSerializer
from django.db import IntegrityError
@csrf_exempt
def get_character_view(request, player_id):
    if request.method == 'GET':
        try:
            character = Characters.objects.get(player_id=player_id)
            return JsonResponse({"id": character.id, "kind": character.kind, "kind_url": character.kind_url}, status=200)
        except Characters.DoesNotExist:
            return JsonResponse({"error": "Character not found"}, status=404)
    return HttpResponseBadRequest("Invalid request method")
# 캐릭터 생성하기
@csrf_exempt
def character_create_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        player_id = data.get('player_id')
        if not player_id:
            return JsonResponse({"error": "Missing player_id"}, status=400)

        # 해당 플레이어의 캐릭터가 이미 존재하는지 확인
        existing_character = Characters.objects.filter(player_id=player_id).first()
        if existing_character:
            return JsonResponse({"error": "Character already exists for this player"}, status=400)

        serializer = CreateCharacterSerializer(data=data)
        if serializer.is_valid():
            try:
                character = serializer.save()
                return JsonResponse({"id": character.id, **serializer.data}, status=201)
            except IntegrityError:
                return JsonResponse({"error": "Character creation failed. Possible duplicate."}, status=400)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'GET':
        return render(request, 'char_create.html')
    return HttpResponseBadRequest("Invalid request method")

@csrf_exempt
def character_update_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        character_id = data.get('character_id')
        new_image_url = data.get('new_image_url')

        if not character_id or not new_image_url:
            return JsonResponse({"error": "Missing character_id or new_image_url"}, status=400)

        try:
            character = Characters.objects.get(pk=character_id)
        except Characters.DoesNotExist:
            return JsonResponse({"error": "Character not found"}, status=404)

        character.kind_url = new_image_url  # Update the image URL
        character.save()
        return JsonResponse({"message": "Character image updated successfully"}, status=200)

    return HttpResponseBadRequest("Invalid request method")

def signup(request):
    return render(request,'signup.html')

def find_account_pwd(request):
    return render(request,'find_account_pwd.html')

def find_account_id(request):
    return render(request,'find_account_id.html')

def find_account(request):
    return render(request,'find_account.html')

def check_id(request):
    return render(request,'check_id.html')

def ranking(request):
    return render(request,'ranking.html')

