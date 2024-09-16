from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from .models import CustomUser
from rest_framework.parsers import MultiPartParser, FormParser
import openpyxl
from django.core.exceptions import ValidationError
from .serializers import ExcelUploadSerializer
from io import BytesIO
import os
from django.core.files.storage import default_storage
from django.conf import settings


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
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "message": "Đăng nhập thành công",
                "token": token.key,  # Trả về token cho người dùng
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Tên đăng nhập hoặc mật khẩu không chính xác"}, status=status.HTTP_401_UNAUTHORIZED)

 
class APIRegisterView(APIView):
    # Không yêu cầu xác thực đối với API này
    authentication_classes = []
    permission_classes = []
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = ExcelUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            workbook = openpyxl.load_workbook(file)
            sheet = workbook.active

            users_created = [] 
            for row in sheet.iter_rows(min_row=2, values_only=True):
                full_name = row[0]  # Assuming the name is in the first column

                if not full_name:
                    continue

                # Tạo user với full_name, username và password đều là user_id
                user = CustomUser(full_name=full_name, role='student')  # Bạn có thể điều chỉnh vai trò nếu cần
                try:
                    user.save()
                    users_created.append({
                        'full_name': full_name,
                        'user_id': user.user_id,
                        'username': user.username,
                        'password': user.user_id  # Password là user_id
                    })
                except ValidationError as e:
                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                    
            # Tạo file Excel với thông tin người dùng
            output = BytesIO()
            workbook_out = openpyxl.Workbook()
            sheet_out = workbook_out.active
            sheet_out.append(['Họ và tên', 'ID', 'Tài khoản', 'Mật khẩu'])

            for user_info in users_created:
                sheet_out.append([
                    user_info['full_name'],
                    user_info['user_id'],
                    user_info['username'],
                    user_info['password']
                ])

            output.seek(0)
            file_name = 'users.xlsx'
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)

            # Save the file to a path accessible by the server
            with default_storage.open(file_path, 'wb+') as destination:
                destination.write(output.getvalue())

            file_url = default_storage.url(file_path)

            return Response({'file_url': file_url}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)