import json

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from economia.models import Characters
from django.http import JsonResponse, HttpResponseBadRequest
from .serializers import CreateCharacterSerializer
from django.db import IntegrityError
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from economia.models import *
import random

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

def generate_verification_code():
    return str(random.randint(100000, 999999))

def find_account_id(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        action = request.POST.get('action', '')

        if action == 'resend':
            verification_code = generate_verification_code()
            VerificationCode.objects.update_or_create(email=email, defaults={'code': verification_code})

            send_mail(
                'Your Verification Code',
                f'Your verification code is {verification_code}.',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return JsonResponse({'status': 'success', 'message': '인증 코드가 전송되었습니다.'})
        
        elif action == 'check':
            try:
                stored_code = VerificationCode.objects.get(email=email).code
                if stored_code == code:
                    user = Player.objects.get(email=email)
                    return JsonResponse({'status': 'success', 'user_id': user.player_id})
                else:
                    return JsonResponse({'status': 'error', 'message': '잘못된 인증 코드입니다.'})
            except VerificationCode.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': '이메일로 발송된 인증 코드가 없습니다.'})

    return render(request, 'find_account_id.html')

def check_id(request, player_id):
    return render(request, 'check_id.html', {'player_id': player_id})