from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Semester, StudyWeek
from .serializers import SemesterSerializer
from datetime import timedelta

class SemesterViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer

    def create(self, request, *args, **kwargs):
        # Lấy dữ liệu từ request
        day_begin = request.data.get('day_begin')
        semester_code = request.data.get('semester')
        number_of_weeks = request.data.get('number_of_weeks')

        # Kiểm tra tính hợp lệ của dữ liệu
        if not day_begin or not semester_code or not number_of_weeks:
            return Response({'error': 'day_begin, semester, and number_of_weeks are required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Parse ngày bắt đầu
        day_begin = parse_date(day_begin)
        
        try:
            number_of_weeks = int(number_of_weeks)
        except ValueError:
            return Response({'error': 'number_of_weeks must be an integer.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Tạo học kỳ mới
        semester = Semester(day_begin=day_begin, semester=semester_code)
        semester.save()

        # Tạo tuần học cho học kỳ mới
        for week in range(1, number_of_weeks + 1):
            StudyWeek.objects.create(semester=semester, week_number=week)

        # Cập nhật ngày kết thúc (day_end) của học kỳ
        semester.day_end = semester.day_begin + timedelta(weeks=number_of_weeks)
        semester.save()

        return Response({'message': 'Semester and study weeks created successfully!'},
                        status=status.HTTP_201_CREATED)