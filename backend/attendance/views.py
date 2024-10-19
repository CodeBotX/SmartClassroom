from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import *
from adminpanel.models import Lesson
from accounts.models import CustomUser
from .serializers import *
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from datetime import timedelta


def get_current_lesson(room, current_time):
        today = current_time.date()
        lessons = Lesson.objects.filter(room=room, day=today)
        for lesson in lessons:
            if lesson.period:
                if lesson.period.start_time <= current_time.time() <= lesson.period.end_time:
                    return lesson  
        return None  

#api điểm danh
# class AttendanceViewSet(viewsets.ModelViewSet):
#     authentication_classes = []
#     permission_classes = []
#     queryset = Attendance.objects.all()
#     serializer_class = AttendanceSerializer
#     def create(self, request, *args, **kwargs):
#         user_id = request.data.get("student_id")  
#         device_id = request.data.get("device_id")

#         if not user_id:
#             return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             device = Device.objects.get(device_id=device_id)
#             room = device.room
#             current_time = timezone.now()

#             lesson = get_current_lesson(room, current_time)

#             if lesson:
#                 user = get_object_or_404(CustomUser, user_id=user_id)
#                 attendance = Attendance(
#                     user=user,  
#                     lesson=lesson,
#                     status=request.data.get("status")
#                 )
#                 attendance.save()  
#                 serializer = self.get_serializer(attendance)
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             else:
#                 return Response({"error": "No active lesson at this time."}, status=status.HTTP_400_BAD_REQUEST)

#         except Device.DoesNotExist:
#             return Response({"error": "Device not found."}, status=status.HTTP_404_NOT_FOUND)
#         except ValidationError as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class AttendanceViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def create(self, request, *args, **kwargs):
        user_id = request.data.get("student_id")  
        device_id = request.data.get("device_id")
        attendance_time = request.data.get("attendance_time")  # Mong đợi thời gian ở định dạng chuỗi

        if not user_id:
            return Response({"error": "Cần có ID người dùng."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            device = Device.objects.get(device_id=device_id)
            room = device.room
            current_time = timezone.now()

            lesson = get_current_lesson(room, current_time)

            if lesson:
                user = get_object_or_404(CustomUser, user_id=user_id)

                # Chuyển đổi attendance_time từ chuỗi sang datetime
                attendance_time = timezone.datetime.fromisoformat(attendance_time)
                lesson_start_time = timezone.datetime.combine(lesson.day, lesson.period.start_time)

                # Xác định trạng thái dựa trên thời gian điểm danh
                if attendance_time <= lesson_start_time + timedelta(minutes=10):
                    status_value = 1  # Có mặt
                elif attendance_time <= lesson_start_time + timedelta(minutes=25):
                    status_value = 2  # Đi muộn
                else:
                    status_value = 3  # Vắng mặt

                attendance = Attendance(
                    user=user,  
                    lesson=lesson,
                    status=status_value
                )
                attendance.save()  
                serializer = self.get_serializer(attendance)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Không có tiết học nào đang hoạt động vào thời điểm này."}, status=status.HTTP_400_BAD_REQUEST)

        except Device.DoesNotExist:
            return Response({"error": "Không tìm thấy thiết bị."}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"error": "Định dạng thời gian điểm danh không hợp lệ."}, status=status.HTTP_400_BAD_REQUEST)

class DeviceViewSet(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def create(self, request, *args, **kwargs):
        device_id = request.data.get('device_id')

        if not device_id or len(device_id) != 9:
            return Response({"error": "Device ID must be 9 characters long."}, status=status.HTTP_400_BAD_REQUEST)

        device, created = Device.objects.get_or_create(device_id=device_id)

        if created:
            return Response(DeviceSerializer(device).data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Device already exists."}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='update-room')
    def update_room(self, request):
        device_id = request.data.get('device_id')
        room_id = request.data.get('room_id')

        if not device_id or not room_id:
            return Response({"error": "Device ID and Room ID are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            device = Device.objects.get(device_id=device_id)
            device.room_id = room_id
            device.save()
            return Response({"message": "Room updated successfully."}, status=status.HTTP_200_OK)
        except Device.DoesNotExist:
            return Response({"error": "Device not found."}, status=status.HTTP_404_NOT_FOUND)


# Hệ thống ghi id vào thẻ 
class RFIDViewSet(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = []
    def start(self, request):
        device_id = request.data.get('device_id')
        try:
            device = Device.objects.get(device_id=device_id)
            room = device.room
            students = room.student.all().values('user__user_id', 'full_name')
            student_list = list(students)  
            return Response({"message": "Đã gửi nhận dữ liệu.", "students": student_list}, status=status.HTTP_200_OK)

        except Device.DoesNotExist:
            return Response({"error": "Không tìm thấy thiết bị."}, status=status.HTTP_404_NOT_FOUND)

    def complete(self, request):
        return Response({"message": "Quá trình ghi RFID đã hoàn thành."}, status=status.HTTP_200_OK)