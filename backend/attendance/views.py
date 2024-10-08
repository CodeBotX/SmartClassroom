from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import *
from .serializers import *
class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def create(self, request, *args, **kwargs):
        student_id = request.data.get("student_id")
        device_id = request.data.get("device_id")
        
        try:
            device = Device.objects.get(device_id=device_id)
            room = device.room
            current_time = timezone.now()

            # Lấy tiết học hiện tại dựa trên ngày và thời gian
            lessons = Lesson.objects.filter(room=room, day=current_time.date(), period__start_time__lte=current_time, period__end_time__gte=current_time)

            if lessons.exists():
                lesson = lessons.first()  # Chọn tiết học đầu tiên phù hợp
                attendance = Attendance.objects.create(
                    student_id=student_id,
                    lesson=lesson,
                    status=request.data.get("status")
                )
                serializer = self.get_serializer(attendance)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "No active lesson at this time."}, status=status.HTTP_400_BAD_REQUEST)

        except Device.DoesNotExist:
            return Response({"error": "Device not found."}, status=status.HTTP_404_NOT_FOUND)
