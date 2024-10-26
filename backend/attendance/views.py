from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import *
from adminpanel.models import Period, Lesson, Semester
from accounts.models import CustomUser
from .serializers import *
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from datetime import timedelta



def get_current_lesson(room, current_time):
    print("đã gọi hàm tìm lesson")
    current_day = current_time.date()
    current_period = Period.objects.filter(
        start_time__lte=current_time.time(),
        end_time__gte=current_time.time()
    ).first()

    if current_period:
        semester_start = Semester.objects.filter(day_begin__lte=current_day).order_by('-day_begin').first()
        semester_end = semester_start.get_day_end() if semester_start else None

        return Lesson.objects.filter(
            room=room,
            day=current_day,
            period=current_period,
            semester=semester_start
        ).first() if semester_start and semester_start.day_begin <= current_day <= semester_end else None
    return None


class AttendanceViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    
    def create(self, request, *args, **kwargs):
        user_id = request.data.get("student_id")  
        device_id = request.data.get("device_id")

        if not user_id:
            return Response({"error": "Cần có ID người dùng."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            device = Device.objects.get(device_id=device_id)
            room = device.room
            current_time = timezone.now() 
            lesson = get_current_lesson(room, current_time)
            if lesson:
                user = get_object_or_404(CustomUser, user_id=user_id)
                attendance_time = current_time
                lesson_start_time = timezone.datetime.combine(lesson.day, lesson.period.start_time)
                lesson_start_time = lesson_start_time.replace(tzinfo=timezone.get_current_timezone())
                if attendance_time <= lesson_start_time + timedelta(minutes=10):
                    status_value = 1  
                else:
                    status_value = 3  
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