from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from .models import CustomUser
import openpyxl
from django.core.exceptions import ValidationError
from .serializers import ExcelUploadSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsAdmin  
from datetime import datetime
from .serializers import *
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.authentication import BasicAuthentication


# API đăng nhập
class ApiLoginView(APIView):
    # Không yêu cầu xác thực đối với API đăng nhập, vì api đăng nhập là điểm đầu tiên mà người dùng truy cập đến 
    # Người dùng chưa đăng nhập thì không có thông tin xác thực để gửi đến server
    authentication_classes = [] #quy định các lớp xác thực được sử dụng để xác thực người dùng
    permission_classes = [] # xác định các lớp phân quyền , người dùng chưa đăng nhập nên loại bỏ phân quyền 
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
            return Response({
                "message": "Đăng nhập thành công",
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Tên đăng nhập hoặc mật khẩu không chính xác"}, status=status.HTTP_401_UNAUTHORIZED)

#  API đăng ký

class APIRegisterView(APIView):
    authentication_classes = [JWTAuthentication]  #JWTAuthentication 
    permission_classes = [IsAuthenticated, IsAdmin]  # IsAuthenticated, IsAdmin

    def post(self, request, *args, **kwargs):

        serializer = ExcelUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            workbook = openpyxl.load_workbook(file)
            sheet = workbook.active

            created_users = 0
            existing_users = 0

            for row in sheet.iter_rows(min_row=2, values_only=True):
                if sheet.title == 'Danh sách giáo viên':
                    ma_dinh_danh = row[1]
                    full_name = row[2]
                    ngay_sinh = row[3]
                    dien_thoai = row[7]
                    vi_tri = row[8]
                    # ma_dinh_danh = row[1] if len(row) > 1 else None
                    # full_name = row[2] if len(row) > 2 else None
                    # ngay_sinh = row[3] if len(row) > 3 else None
                    # dien_thoai = row[7] if len(row) > 7 else None
                    # vi_tri = row[8] if len(row) > 8 else None

                    if not ma_dinh_danh or not full_name:
                        continue

                    if vi_tri:
                        if vi_tri.lower() == 'giáo viên':
                            role = 'teacher'
                        elif vi_tri.lower() == 'cán bộ quản lý':
                            role = 'admin'
                        else:
                            continue  # Bỏ qua nếu vi_tri không khớp

                elif sheet.title == 'Danh sách học sinh':
                    ma_dinh_danh = row[2]
                    full_name = row[3]
                    ngay_sinh = row[4]


                    if not ma_dinh_danh or not full_name:
                        continue
                    
                    role = 'student'

                elif sheet.title == 'Danh sách phụ huynh':
                    ma_dinh_danh = None
                    full_name = row[1]
                    dien_thoai = row[2]

                    if not full_name or not dien_thoai:
                        continue
                    
                    role = 'parent'
                    ma_dinh_danh = dien_thoai
                
                # Định dạng ngày sinh
                if ngay_sinh:
                    try:
                        ngay_sinh = datetime.strptime(ngay_sinh, '%d/%m/%Y').date()
                    except ValueError:
                        continue  # Bỏ qua nếu định dạng ngày sinh không hợp lệ

                # Kiểm tra nếu mã định danh đã tồn tại
                if CustomUser.objects.filter(user_id=ma_dinh_danh).exists():
                    existing_users += 1
                    continue

                # Tạo user
                user = CustomUser(
                    full_name=full_name,
                    username=ma_dinh_danh if ma_dinh_danh else None,
                    user_id=ma_dinh_danh,
                    role=role,
                    phone_number=dien_thoai if role in ['teacher', 'admin','parent'] else None,
                    date_of_birth=ngay_sinh if role in ['teacher', 'student','admin'] else None
                )
                try:
                    user.save()
                    created_users += 1
                except ValidationError as e:
                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            if created_users > 0:
                return Response({"detail": f"Tài khoản đã được tạo thành công. Số tài khoản mới: {created_users}."}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Không có tài khoản mới được tạo."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]  # không yêu cầu xác thực
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        # Lấy người dùng từ request.user (người đã đăng nhập)
        user = request.user
        # Bạn có thể dùng serializer để định dạng thông tin người dùng nếu cần
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)

class UserUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def patch(self, request, *args, **kwargs):
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)  # Partial update

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)