from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model, authenticate
from django.views.decorators.http import require_GET

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from datetime import datetime, timedelta
import jwt
import json

User = get_user_model()

@csrf_exempt
@require_GET
def supervise(request):
    return HttpResponse("<h1>RecoImageApp API is running</h1>", content_type="text/html")

# メール認証用関数
def send_verification_email(user):
    verification_code = get_random_string(length=32)  # 任意のランダムなコードを生成
    user.verification_code = verification_code  # verification_codeをユーザーに保存
    user.save()

    verification_url = f'{settings.API_FRONTEND_URL}/verify_email/{verification_code}/'  # フロントエンドの認証URL
    
    # 認証メールを送信
    send_mail(
        'Please verify your email address',
        f'Click this link to verify your email: {verification_url}',
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )

# サインアップ処理
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')

        if User.objects.filter(email=email).exists():
            return JsonResponse({'message': 'このメールはすでに使用されています。'}, status=400)

        # ユーザー作成（アクティブではない）
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name,
            is_active=False  # 認証されるまで無効
        )
        user.save()

        # メール認証を送信
        send_verification_email(user)

        return JsonResponse({'message': '認証メールを送信しました。メールをご確認ください。'})

    return JsonResponse({'error': 'Invalid request method.'}, status=400)

# メール認証用ビュー
@csrf_exempt
def verify_email(request, verification_code):
    # verification_codeに基づいてユーザーを検索
    user = User.objects.filter(verification_code=verification_code).first()
    
    if user:
        # ユーザーが見つかった場合、認証コードを無効化し、アクティブにする
        user.is_active = True
        user.verification_code = None  # verification_codeをクリア
        user.save()
        return JsonResponse({'message': 'メール認証が完了しました。ログインできます。'})
    else:
        # ユーザーが見つからなかった場合
        return JsonResponse({'error': '無効な確認リンクです。'}, status=400)
        

# ログイン処理
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'message': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'message': 'Invalid email or password.'}, status=status.HTTP_401_UNAUTHORIZED)

    user = authenticate(username=user.username, password=password)
    if user is None:
        return Response({'message': 'Invalid email or password.'}, status=status.HTTP_401_UNAUTHORIZED)

    # JWTトークン生成
    payload = {
        'id': user.id,
        'username': user.username,
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    return Response({'token': token})
