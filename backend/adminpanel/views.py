
# -----------------------------------------------sử dụng viewset-----------------------------------------------

from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.decorators import action
from django.db import transaction
from datetime import timedelta
from .filters import LessonFilter 
from django_filters.rest_framework import DjangoFilterBackend
from accounts.models import Student
from django.db.models import Avg




#api set kì học
class SemesterViewSet(viewsets.ModelViewSet):
    authentication_classes  = []
    permission_classes = []
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer


    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

        

#api set điểm, có thể thêm cùng lúc nhiều học sinh
class GradesViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = Grades.objects.all()
    serializer_class = GradesSerializer

    @transaction.atomic  
    def create(self, request, *args, **kwargs):
        data = request.data

        # Nếu `data` là một danh sách (nhiều điểm)
        if isinstance(data, list):
            serializer = GradesSerializer(data=data, many=True)
        else:
            # Nếu chỉ là một đối tượng (trường hợp thêm một điểm)
            serializer = GradesSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def list(self, request):
        # Lấy các tham số từ query parameters
        semester_name = request.query_params.get('semester_name')
        room_name = request.query_params.get('room_name')
        subject = request.query_params.get('subject')

        if not semester_name or not room_name or not subject:
            return Response({'error': 'Thiếu các tham số: semester_name, room_name hoặc subject.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Tìm room và semester theo tên
            room = Room.objects.get(name=room_name)
            semester = Semester.objects.get(name=semester_name)

            # Lấy danh sách học sinh trong room
            students = room.students.all()

            results = {}
            no_scores = []  # Danh sách lưu học sinh không có điểm

            for student in students:
                # Tính điểm trung bình cho từng học sinh theo môn và học kỳ
                average_score = Grades.objects.filter(
                    student=student,
                    subject=subject,
                    semester=semester
                ).aggregate(avg_score=Avg('grade'))['avg_score']  # Trả về None nếu không có điểm

                if average_score is None:
                    no_scores.append(student.full_name)  # Thêm học sinh không có điểm vào danh sách
                else:
                    results[student.full_name] = average_score  # Chỉ thêm vào kết quả nếu có điểm

            # Sắp xếp danh sách theo điểm trung bình từ cao xuống thấp
            sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)

            # Nếu có học sinh không có điểm, trả về thông báo
            return Response({
                'sorted_results': sorted_results,
                'no_scores': no_scores  # Danh sách học sinh không có điểm
            }, status=status.HTTP_200_OK)

        except Room.DoesNotExist:
            return Response({'error': 'Room không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)
        except Semester.DoesNotExist:
            return Response({'error': 'Học kỳ không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)
    
    
class PlannedLessonViewSet(viewsets.ModelViewSet):
    authencation_classes = []
    permission_classes = []
    queryset = PlannedLesson.objects.all()
    serializer_class = PlannedLessonSerializer
    def create(self, request):
        serializer = PlannedLessonSerializer(data=request.data)
        if serializer.is_valid():
            semester = serializer.validated_data['semester'] # Liên kết
            subject = serializer.validated_data['subject'] #choice
            lesson_number = serializer.validated_data['lesson_number']
            name_lesson = serializer.validated_data['name_lesson']
            rooms = serializer.validated_data['rooms'] # Liên kết
            if subject not in SubjectChoices.values:
                return Response({'error': 'Không tồn tại môn học.'}, status=status.HTTP_400_BAD_REQUEST)
            with transaction.atomic():
                for room in rooms:
                    PlannedLesson.objects.create(
                        semester=semester,
                        subject=subject,
                        lesson_number=lesson_number,
                        name_lesson=name_lesson,
                        room=room
                    )
            return Response({'message': 'Lessons created successfully.'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LessonViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = Lesson.objects.all() 
    serializer_class = LessonSerializer 
    # 1. Create Schedule (Thời khóa biểu)
    @action(detail=False, methods=['post'], url_path='create_schedule')
    @transaction.atomic
    def create_schedule(self, request):
        semester_id = request.data.get('semester')
        room_id = request.data.get('room')
        weekday = request.data.get('weekday')
        period_id = request.data.get('period')
        subject = request.data.get('subject')

        # Get the semester
        try:
            semester = Semester.objects.get(name=semester_id)
        except Semester.DoesNotExist:
            return Response({"error": "Semester not found."}, status=status.HTTP_404_NOT_FOUND)

        # Get the period
        try:
            period = Period.objects.get(number=period_id)
        except Period.DoesNotExist:
            return Response({"error": "Period not found."}, status=status.HTTP_404_NOT_FOUND)

        start_date = semester.day_begin
        end_date = semester.get_day_end()
        
        lessons_created = []

        # Iterate over the weeks in the semester
        current_date = start_date
        while current_date <= end_date:
            # Check if the current_date is the desired weekday
            if current_date.weekday() == weekday:
                lesson = Lesson(
                    semester=semester,
                    subject=subject,
                    room_id=room_id,
                    day=current_date,
                    period=period
                )
                lesson.save()
                lessons_created.append(lesson)

            current_date += timedelta(days=1)

        # Serialize the created lessons for the response
        serializer = LessonSerializer(lessons_created, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # 2. Update Lesson Details
    @action(detail=True, methods=['patch'], url_path='update')
    def update_lesson(self, request, pk=None):
        try:
            lesson = Lesson.objects.get(pk=pk)
        except Lesson.DoesNotExist:
            return Response({"error": "Lesson not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = LessonSerializer(lesson, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    filter_backends = [DjangoFilterBackend]
    filterset_class = LessonFilter
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


#lấy điểm của 1 học sinh theo từng môn học
class StudentGradesViewSet(viewsets.ViewSet):
    """
    API để lấy danh sách điểm của một học sinh theo từng môn trong cùng một học kỳ.
    """
    def list(self, request, user_id):
        semester_name = request.query_params.get('semester_name')

        if not semester_name:
            return Response({'error': 'Thiếu semester_name.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = Student.objects.get(user__user_id=user_id)
            semester = Semester.objects.get(name=semester_name)  # Tìm kiếm học kỳ theo tên

            grades = Grades.objects.filter(student=student, semester=semester)
            serializer = GradesSerializer(grades, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({'error': 'Học sinh không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)
        except Semester.DoesNotExist:
            return Response({'error': 'Học kỳ không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)
        

# top 30 học sinh trong môn học trong 1 học kỳ
class TopStudentsViewSet(viewsets.ViewSet):
    """
    API để lấy danh sách 30 học sinh dẫn đầu theo môn học trong cùng một học kỳ.
    """
    def list(self, request):
        semester_name = request.query_params.get('semester_name')  
        subject = request.query_params.get('subject')  

        if not semester_name:
            return Response({'error': 'Thiếu semester_name.'}, status=status.HTTP_400_BAD_REQUEST)

        if not subject:
            return Response({'error': 'Thiếu môn học.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
           
            semester = Semester.objects.get(name=semester_name)

            
            if subject not in SubjectChoices.values:
                return Response({'error': 'Môn học không hợp lệ.'}, status=status.HTTP_400_BAD_REQUEST)

         
            students = Grades.objects.filter(subject=subject, semester=semester)\
                .values('student__full_name')\
                .annotate(avg_score=Avg('grade'))\
                .order_by('-avg_score')[:30]

            return Response({'top_students': list(students)}, status=status.HTTP_200_OK)

        except Semester.DoesNotExist:
            return Response({'error': 'Học kỳ không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)