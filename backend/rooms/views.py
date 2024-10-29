from rest_framework import viewsets
from .models import Room, SeatingPosition
from .serializers import *
from rest_framework.response import Response
from rest_framework import status 
from accounts.models import Student
from rest_framework.decorators import action
from rest_framework import generics
# api room
class RoomViewSet(viewsets.ModelViewSet):
    authencation_classes = []
    permission_classes = []
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    # chưa check lớp học đã tồn tại
    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        if not name:
            return Response({'error': 'Lớp học đã tồn tại.'}, status=status.HTTP_400_BAD_REQUEST)
        room = Room.objects.create(name=name)
        serializer = self.get_serializer(room)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def update(self, request, *args, **kwargs):
        room = self.get_object()
        serializer = self.get_serializer(room, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def get_queryset(self):
        return super().get_queryset()

    @action(detail=False, methods=['post'], url_path='addstudents')
    def add_students(self, request, *args, **kwargs):
        # Lấy tên lớp học từ request body
        room_name = request.data.get('room')

        if not room_name:
            return Response({'error': 'Room name is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Tìm lớp học theo tên
        try:
            room = Room.objects.get(name=room_name)
        except Room.DoesNotExist:
            return Response({'error': 'Room not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Lấy danh sách ID học sinh từ request
        student_ids = request.data.get('students', [])

        if not student_ids:
            return Response({'error': 'No student IDs provided.'}, status=status.HTTP_400_BAD_REQUEST)

        # Lọc các học sinh hợp lệ từ model Student
        students = Student.objects.filter(user_id__in=student_ids)
        invalid_student_ids = set(student_ids) - set(students.values_list('user_id', flat=True))

        if invalid_student_ids:
            return Response({
                'error': 'Some students are invalid.',
                'invalid_student_ids': list(invalid_student_ids)
            }, status=status.HTTP_404_NOT_FOUND)

        # Thêm học sinh vào lớp
        room.students.add(*students)

        return Response({'message': 'Students added successfully.'}, status=status.HTTP_200_OK)

    


# api chỗ ngồi
class SeatingPositionViewSet(viewsets.ModelViewSet):
    authencation_classes = []
    permission_classes = []
    queryset = SeatingPosition.objects.all()
    serializer_class = SeatingPositionSerializer
    @action(detail=False, methods=['post'])
    def swap_seats(self, request):
        user_id_1 = request.data.get('user_id_1')
        user_id_2 = request.data.get('user_id_2')

        try:
            # Lấy chỗ ngồi của hai học sinh
            seating_position_1 = SeatingPosition.objects.get(student__user__user_id=user_id_1)
            seating_position_2 = SeatingPosition.objects.get(student__user__user_id=user_id_2)

            # Lưu thông tin học sinh và chỗ ngồi
            student_1 = seating_position_1.student
            student_2 = seating_position_2.student

            room_1 = seating_position_1.room
            row_1 = seating_position_1.row
            column_1 = seating_position_1.column

            room_2 = seating_position_2.room
            row_2 = seating_position_2.row
            column_2 = seating_position_2.column

            # Xóa hai chỗ ngồi hiện tại
            seating_position_1.delete()
            seating_position_2.delete()

            # Tạo lại chỗ ngồi với thông tin đã hoán đổi
            new_position_1 = SeatingPosition.objects.create(student=student_2, room=room_1, row=row_1, column=column_1)
            new_position_2 = SeatingPosition.objects.create(student=student_1, room=room_2, row=row_2, column=column_2)

            return Response({
                'message': 'Seats swapped successfully',
                'student_1_new_position': {
                    'room': new_position_1.room.name,
                    'row': new_position_1.row,
                    'column': new_position_1.column
                },
                'student_2_new_position': {
                    'room': new_position_2.room.name,
                    'row': new_position_2.row,
                    'column': new_position_2.column
                }
            }, status=status.HTTP_200_OK)

        except SeatingPosition.DoesNotExist:
            return Response({'error': 'One or both students do not have seating positions'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SeatingPositionListView(generics.ListAPIView):
    authencation_classes = []
    permission_classes = [] 
    serializer_class = SeatingPositionSerializer

    def get_queryset(self):
        room_name = self.kwargs['room_name']
        try:
            room = Room.objects.get(name=room_name)
            return SeatingPosition.objects.filter(room=room)
        except Room.DoesNotExist:
            return SeatingPosition.objects.none()  

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"detail": "Room not found or no seating positions available."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    