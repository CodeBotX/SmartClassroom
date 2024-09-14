from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class LoginView(APIView):
    # Không yêu cầu xác thực đối với API đăng nhập
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        # Kiểm tra nếu người dùng đã đăng nhập
        if request.user.is_authenticated:
            return Response({"error": "Bạn đã đăng nhập"}, status=status.HTTP_400_BAD_REQUEST)

        # Lấy thông tin username và password từ request
        username = request.data.get('username')
        password = request.data.get('password')

        # Xác thực người dùng
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Đăng nhập người dùng
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "message": "Đăng nhập thành công",
                "token": token.key,  # Trả về token cho người dùng
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Tên đăng nhập hoặc mật khẩu không chính xác"}, status=status.HTTP_401_UNAUTHORIZED)
