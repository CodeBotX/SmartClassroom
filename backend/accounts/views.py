from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response
from rest_framework import status,views
from django.contrib.auth import authenticate, login
from .models import *
import openpyxl
from django.core.exceptions import ValidationError
from .serializers import ExcelUploadSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication  
from datetime import datetime
from .serializers import *
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from openpyxl import load_workbook


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

        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            return Response({
                "message": "Đăng nhập thành công",
                "access_token": access_token,  
                "refresh_token": refresh_token  
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Tên đăng nhập hoặc mật khẩu không chính xác"}, status=status.HTTP_401_UNAUTHORIZED)
        
#--------------------------------------API Đăng Ký-------------------------------------------------------
# Api đăng kí giáo viên
class APIRegisterTeacherView(APIView):
    authentication_classes = []  # JWTAuthentication 
    permission_classes = []  # IsAuthenticated, IsAdmin

    def post(self, request, *args, **kwargs):
        serializer = ExcelUploadSerializer(data=request.FILES)  # Đọc file từ request.FILES
        if serializer.is_valid():
            file = serializer.validated_data['file']
            workbook = openpyxl.load_workbook(file)
            sheet = workbook["Danh sách giáo viên"]

            created_users = 0
            existing_users = 0

            for row in sheet.iter_rows(min_row=2, values_only=True):
                # Lấy dữ liệu từ các cột tương ứng
                ma_dinh_danh = row[1]
                full_name = row[2]
                ngay_sinh = row[3]
                gioi_tinh = row[4]
                dan_toc = row[6]
                dien_thoai = row[7]
                vi_tri = row[8]  # Giáo viên hoặc Cán bộ quản lý

                # Bỏ qua hàng không đủ thông tin cần thiết
                if not ma_dinh_danh or not full_name or not vi_tri:
                    continue

                # Phân loại role theo vị trí việc làm
                is_teacher = vi_tri.lower() == 'giáo viên'
                is_admin = vi_tri.lower() == 'cán bộ quản lý'
                
                if not is_teacher and not is_admin:
                    continue  # Bỏ qua nếu vị trí không hợp lệ

                # Kiểm tra nếu người dùng đã tồn tại
                if CustomUser.objects.filter(user_id=ma_dinh_danh).exists():
                    existing_users += 1
                    continue

                # Kiểm tra ngày sinh
                if ngay_sinh:
                    try:
                        ngay_sinh = datetime.strptime(ngay_sinh, '%d/%m/%Y').date()
                    except ValueError:
                        continue  # Bỏ qua nếu định dạng ngày sinh không hợp lệ

                # Tạo CustomUser
                user = CustomUser(
                    full_name=full_name,
                    username=ma_dinh_danh,  # Username sẽ là mã định danh
                    user_id=ma_dinh_danh,
                    sex=gioi_tinh,
                    nation=dan_toc,
                    phone_number=dien_thoai,
                    day_of_birth=ngay_sinh,
                    is_teacher=is_teacher,
                    is_admin=is_admin,
                )

                try:
                    user.save()

                    # Tạo đối tượng Teacher hoặc Admin
                    if is_teacher:
                        Teacher.objects.create(
                            user=user,
                            active_status=row[5],  # Trạng thái
                            contract_types=row[10],  # Hình thức hợp đồng
                            expertise_levels=row[11],  # trình độ chuyên môn
                            subjects=row[12]  # Môn dạy
                        )
                    elif is_admin:
                        Admin.objects.create(
                            user=user,
                            active_status=row[5],  # Trạng thái
                            contract_types=row[10],  # Hình thức hợp đồng
                            expertise_levels=row[11],  #trình độ chuyên môn
                            description=row[9]  # Mô tả
                        )

                    created_users += 1
                except ValidationError as e:
                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            # Trả về kết quả sau khi xử lý
            if created_users > 0:
                return Response({"detail": f"Tạo thành công {created_users} tài khoản giáo viên/cán bộ quản lý."}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Không có tài khoản mới được tạo."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Api đăng ký học sinh
class APIRegisterStudentView(APIView):
    authentication_classes = []  # JWTAuthentication 
    permission_classes = []  # IsAuthenticated, IsAdmin

    def post(self, request, *args, **kwargs):
        serializer = ExcelUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            workbook = openpyxl.load_workbook(file)
            sheet = workbook["Danh sách học sinh"]

            created_students = 0
            existing_students = 0

            for row in sheet.iter_rows(min_row=7, values_only=True):
                # Lấy dữ liệu từ các cột tương ứng
                ma_dinh_danh = row[2]
                full_name = row[3]
                ngay_sinh = row[4]
                gioi_tinh = row[5]
                dan_toc = row[6]
                active_status = row[7]  # Trạng thái

                # Bỏ qua hàng không đủ thông tin cần thiết
                if not ma_dinh_danh or not full_name:
                    continue

                # Kiểm tra nếu người dùng đã tồn tại
                if CustomUser.objects.filter(user_id=ma_dinh_danh).exists():
                    existing_students += 1
                    continue

                # Kiểm tra ngày sinh
                if ngay_sinh:
                    try:
                        ngay_sinh = datetime.strptime(ngay_sinh, '%d/%m/%Y').date()
                    except ValueError:
                        continue  # Bỏ qua nếu định dạng ngày sinh không hợp lệ

                # Tạo CustomUser cho học sinh
                user = CustomUser(
                    full_name=full_name,
                    username=ma_dinh_danh,  # Username sẽ là mã định danh
                    user_id=ma_dinh_danh,
                    sex=gioi_tinh,
                    nation=dan_toc,
                    day_of_birth=ngay_sinh,
                    is_student=True,  # Đánh dấu là học sinh
                )

                try:
                    user.save()
                    # Tạo đối tượng Student
                    Student.objects.create(
                        user=user,
                        room=None,  # Hoặc có thể thêm logic để lấy thông tin phòng
                        parent=None,  # Hoặc có thể thêm logic để gán phụ huynh
                        active_status = active_status  # Trạng thái
                    )

                    created_students += 1
                except ValidationError as e:
                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            # Trả về kết quả sau khi xử lý
            if created_students > 0:
                return Response({"detail": f"Tạo thành công {created_students} tài khoản học sinh."}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Không có tài khoản mới được tạo."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class APIRegisterParentView(APIView):
    authentication_classes = []  # JWTAuthentication 
    permission_classes = []  # IsAuthenticated, IsAdmin

    def post(self, request, *args, **kwargs):
        serializer = ExcelUploadSerializer(data=request.FILES)  # Đọc file từ request.FILES
        if serializer.is_valid():
            file = serializer.validated_data['file']
            workbook = openpyxl.load_workbook(file)
            sheet = workbook["Danh sách phụ huynh"]  # Tên sheet trong file excel

            created_parents = 0
            existing_parents = 0  # tài khoản tồn tại
            invalid_students = 0  # không có học sinh tương ứng
            added_students_info = []
            added_students_messages = []
            for row in sheet.iter_rows(min_row=5, values_only=True):
                # Lấy dữ liệu từ các cột tương ứng
                full_name = row[1]
                phone_number = row[2]
                address = row[3]
                ma_dinh_danh_hoc_sinh = row[4]

                # Bỏ qua hàng không đủ thông tin cần thiết
                if not full_name or not phone_number or not ma_dinh_danh_hoc_sinh:
                    continue

                # Kiểm tra học sinh có tồn tại không
                try:
                    ma_dinh_danh_hoc_sinh = str(ma_dinh_danh_hoc_sinh).strip()
                    student = Student.objects.get(user__user_id=ma_dinh_danh_hoc_sinh)
                except Student.DoesNotExist:
                    # Nếu học sinh không tồn tại, bỏ qua
                    invalid_students += 1
                    print(f"Học sinh với mã định danh {ma_dinh_danh_hoc_sinh} không tồn tại.")
                    continue

                # Kiểm tra nếu phụ huynh đã tồn tại
                parent_user = CustomUser.objects.filter(username=phone_number, is_parent=True).first()

                if parent_user:
                    # Nếu phụ huynh đã tồn tại mà học sinh chưa được liên kết với phụ huynh đó, bỏ qua
                    if not student.parent:
                        student.parent = parent_user.parent
                        student.save()
                    existing_parents += 1
                    continue

                # Tạo CustomUser cho phụ huynh nếu phụ huynh chưa tồn tại
                user = CustomUser(
                    full_name=full_name,
                    username=phone_number,
                    user_id=phone_number,  # Username sẽ là số điện thoại
                    phone_number=phone_number,
                    is_parent=True,
                )
                user.set_password(phone_number)  # Sử dụng số điện thoại làm password

                # Lưu đối tượng phụ huynh
                user.save()

                # Tạo đối tượng Parent
                parent = Parent.objects.create(
                    user=user,
                    address=address
                )

                # Cập nhật mối quan hệ giữa phụ huynh và học sinh
                student.parent = parent
                student.save()

                created_parents += 1
                
                for info in added_students_info:
                    added_students_messages.append(f"Đã thêm học sinh {info['student_user_id']} cho phụ huynh {info['parent_user_id']}.")

            # Trả về kết quả sau khi xử lý
            return Response({
                "detail": f"Tạo thành công {created_parents} tài khoản phụ huynh.",
                "existing_parents": existing_parents,
                "invalid_students": invalid_students,
                "added_students_messages": added_students_messages,
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------------------------------------------------------------------------



# api lấy thông tin user
class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user

        # Serialize base user data
        user_data = UserSerializer(user).data

        # Check the user's role and add role-specific data
        if user.is_teacher:
            try:
                teacher = user.teacher
                teacher_data = TeacherSerializer(teacher).data
                user_data.update(teacher_data)
            except Teacher.DoesNotExist:
                return Response({'error': 'Teacher profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        elif user.is_admin:
            try:
                admin = user.admin
                admin_data = AdminSerializer(admin).data
                user_data.update(admin_data)
            except Admin.DoesNotExist:
                return Response({'error': 'Admin profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        elif user.is_parent:
            try:
                parent = user.parent
                parent_data = ParentSerializer(parent).data
                user_data.update(parent_data)
            except Parent.DoesNotExist:
                return Response({'error': 'Parent profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        elif user.is_student:
            try:
                student = user.student
                student_data = StudentSerializer(student).data
                user_data.update(student_data)
            except Student.DoesNotExist:
                return Response({'error': 'Student profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        return Response(user_data, status=status.HTTP_200_OK)

# ---------------------------------------------------------------------------------------------

#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def patch(self, request, *args, **kwargs):
#         user = request.user
#         # Xác định serializer dựa trên vai trò của người dùng
#         if user.is_teacher:
#             serializer = TeacherUpdateSerializer(user.teacher, data=request.data, partial=True)
#         elif user.is_admin:
#             serializer = AdminUpdateSerializer(user.admin, data=request.data, partial=True)
#         elif user.is_parent:
#             serializer = ParentUpdateSerializer(user.parent, data=request.data, partial=True)
#         elif user.is_student:
#             serializer = StudentUpdateSerializer(user.student, data=request.data, partial=True)
#         else:
#             serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        user = request.user
        
        if user.is_teacher:
            serializer = TeacherUpdateSerializer(user.teacher, data=request.data, partial=True)
        elif user.is_admin:
            serializer = AdminUpdateSerializer(user.admin, data=request.data, partial=True)
        elif user.is_parent:
            serializer = ParentUpdateSerializer(user.parent, data=request.data, partial=True)
        elif user.is_student:
            serializer = StudentUpdateSerializer(user.student, data=request.data, partial=True)
        else:
            serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# api đổi mật khẩu
class ChangePasswordView(APIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"detail": "Mật khẩu đã được thay đổi thành công."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -------------------------------------------------------------------------------------------

class AdminPasswordResetView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not request.user.is_admin:  # Kiểm tra quyền admin
            return Response({"detail": "Bạn không có quyền thực hiện thao tác này."}, status=status.HTTP_403_FORBIDDEN)

        serializer = AdminPasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            try:
                user = CustomUser.objects.get(user_id=user_id)
                new_password = user.user_id  # Reset mật khẩu về mã định danh
                user.set_password(new_password)
                user.save()
                return Response({"detail": f"Mật khẩu của người dùng {user.full_name} đã được reset thành công."}, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response({"error": "Người dùng không tồn tại."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
