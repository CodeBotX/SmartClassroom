
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
from accounts.models import Student,Teacher
from django.db.models import Avg
from collections import defaultdict

class SemesterViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer

    def create(self, request, *args, **kwargs):
        day_begin = request.data.get('day_begin')

        if day_begin:
            day_begin_date = date.fromisoformat(day_begin)
            if day_begin_date.weekday() != 0: 
                return Response({"error": "Ngày bắt đầu phải là thứ Hai."},
                                status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save()

class GradesViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = Grades.objects.all()
    serializer_class = GradesSerializer

    @transaction.atomic  
    def create(self, request, *args, **kwargs):
        data = request.data
        if isinstance(data, list):
            serializer = GradesSerializer(data=data, many=True)
        else:
            serializer = GradesSerializer(data=data)

        if serializer.is_valid():
            if isinstance(data, list):
                for item in data:
                    student = item.get('student')
                    subject = item.get('subject')
                    semester = item.get('semester')
                    score_type = item.get('score_type')
                    if score_type in [ScoreType.GK, ScoreType.CK]:
                        existing_grade = Grades.objects.filter(
                            student=student, subject=subject, semester=semester, score_type=score_type
                        ).exists()
                        if existing_grade:
                            return Response(
                                {"detail": f"Điểm {score_type} đã tồn tại cho học sinh {student} trong môn {subject}."},
                                status=status.HTTP_400_BAD_REQUEST
                            )
            else:
                student = serializer.validated_data.get('student')
                subject = serializer.validated_data.get('subject')
                semester = serializer.validated_data.get('semester')
                score_type = serializer.validated_data.get('score_type')

                if score_type in [ScoreType.GK, ScoreType.CK]:
                    existing_grade = Grades.objects.filter(
                        student=student, subject=subject, semester=semester, score_type=score_type
                    ).exists()
                    if existing_grade:
                        return Response(
                            {"detail": f"Điểm {score_type} đã tồn tại cho học sinh {student} trong môn {subject}."},
                            status=status.HTTP_400_BAD_REQUEST
                        )

            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """
        List method để xử lý các API lấy danh sách điểm học sinh, 
        top học sinh và điểm theo phòng học.
        """
        user_id = request.query_params.get('user_id')
        semester_name = request.query_params.get('semester_name')
        subject = request.query_params.get('subject')
        room_name = request.query_params.get('room_name')
        score_type = request.query_params.get('score_type')
        top_students = request.query_params.get('top_students')

        if not semester_name:
            return Response({'error': 'Thiếu semester_name.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            semester = Semester.objects.get(name=semester_name)

            if user_id:
                try:
                    student = Student.objects.get(user__user_id=user_id)
                    grades_query = Grades.objects.filter(student=student, semester=semester)

                    if score_type:
                        grades_query = grades_query.filter(score_type=score_type)

                    serializer = GradesSerializer(grades_query, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except Student.DoesNotExist:
                    return Response({'error': 'Học sinh không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)
            elif room_name:
                try:
                    room = Room.objects.get(name=room_name)
                    students = room.students.all()

                    results = {}
                    no_scores = []  

                    for student in students:
                        average_score = Grades.objects.filter(
                            student=student,
                            subject=subject,
                            semester=semester
                        ).aggregate(avg_score=Avg('grade'))['avg_score']

                        if average_score is None:
                            no_scores.append(student.full_name)
                        else:
                            results[student.full_name] = average_score

                    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
                    return Response({
                        'sorted_results': sorted_results,
                        'no_scores': no_scores
                    }, status=status.HTTP_200_OK)

                except Room.DoesNotExist:
                    return Response({'error': 'Room không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)
            elif top_students:
                if subject not in SubjectChoices.values:
                    return Response({'error': 'Môn học không hợp lệ.'}, status=status.HTTP_400_BAD_REQUEST)

                students = Grades.objects.filter(subject=subject, semester=semester)\
                    .values('student__full_name')\
                    .annotate(avg_score=Avg('grade'))\
                    .order_by('-avg_score')[:30]

                return Response({'top_students': list(students)}, status=status.HTTP_200_OK)

            else:
                return Response({'error': 'Thiếu các tham số bắt buộc.'}, status=status.HTTP_400_BAD_REQUEST)

        except Semester.DoesNotExist:
            return Response({'error': 'Học kỳ không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)
    @action(detail=False, methods=['get'], url_path='statistics')
    def get_statistics(self, request):
        semester_name = request.query_params.get('semester_name')
        room_name = request.query_params.get('room_name')
        subject = request.query_params.get('subject')
        score_type = request.query_params.get('score_type')  # Nhận loại điểm từ tham số

        if not semester_name or not room_name or not subject or not score_type:
            return Response({'error': 'Thiếu các tham số: semester_name, room_name, subject hoặc score_type.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            room = Room.objects.get(name=room_name)
            semester = Semester.objects.get(name=semester_name)

            # Lấy danh sách học sinh trong room
            students = room.students.all()

            # Khởi tạo dictionary để lưu trữ số lượng cho mỗi khoảng
            grade_ranges = defaultdict(int)

            # Thiết lập các khoảng điểm
            step = 0.5
            for i in range(0, 10):
                grade_ranges[f'{i}-{i + step}'] = 0

            for student in students:
                # Lấy tất cả điểm theo loại điểm từ tham số
                grades = Grades.objects.filter(
                    student=student,
                    subject=subject,
                    semester=semester,
                    score_type=score_type  # Lọc theo loại điểm
                ).values_list('grade', flat=True)

                # Tính số lượng điểm cho mỗi khoảng
                for grade in grades:
                    for i in range(0, 10):
                        if i <= grade < i + step:
                            grade_ranges[f'{i}-{i + step}'] += 1
                            break

            return Response(grade_ranges, status=status.HTTP_200_OK)

        except Room.DoesNotExist:
            return Response({'error': 'Room không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)
        except Semester.DoesNotExist:
            return Response({'error': 'Học kỳ không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)
        except Grades.DoesNotExist:
            return Response({'error': 'Loại điểm không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)

class PlannedLessonViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = PlannedLesson.objects.all()
    serializer_class = PlannedLessonSerializer

    def create(self, request):
        serializer = PlannedLessonSerializer(data=request.data)
        if serializer.is_valid():
            semester = serializer.validated_data['semester']
            subject = serializer.validated_data['subject']
            lesson_number = serializer.validated_data['lesson_number']
            name_lesson = serializer.validated_data['name_lesson']
            rooms = serializer.validated_data['rooms']  # Lưu ý sử dụng 'rooms'

            if subject not in SubjectChoices.values:
                return Response({'error': 'Môn học không tồn tại.'}, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                for room in rooms:
                    PlannedLesson.objects.create(
                        semester=semester,
                        subject=subject,
                        lesson_number=lesson_number,
                        name_lesson=name_lesson,
                        room=room
                    )
            return Response({'message': 'Tạo bài học thành công.'}, status=status.HTTP_201_CREATED)

        # Thông báo lỗi bằng tiếng Việt
        errors = {}
        for field, messages in serializer.errors.items():
            if field == 'semester':
                errors[field] = ['Khóa không hợp lệ - đối tượng không tồn tại.']
            elif field == 'subject':
                errors[field] = ['Môn học không hợp lệ.']
            elif field == 'rooms':
                errors[field] = ['Không tìm thấy phòng học.']
            else:
                errors[field] = messages

        return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            serializer.save()
            rooms = serializer.validated_data['rooms']

            if instance.subject not in SubjectChoices.values:
                return Response({'error': 'Môn học không tồn tại.'}, status=status.HTTP_400_BAD_REQUEST)

            # Cập nhật thông tin bài học
            for room in rooms:
                PlannedLesson.objects.update_or_create(
                    semester=serializer.validated_data['semester'],
                    subject=serializer.validated_data['subject'],
                    lesson_number=serializer.validated_data['lesson_number'],
                    name_lesson=serializer.validated_data['name_lesson'],
                    room=room
                )
            return Response({'message': 'Cập nhật bài học thành công.'}, status=status.HTTP_200_OK)

        # Thông báo lỗi bằng tiếng Việt
        errors = {}
        for field, messages in serializer.errors.items():
            if field == 'semester':
                errors[field] = ['Khóa không hợp lệ - đối tượng không tồn tại.']
            elif field == 'subject':
                errors[field] = ['Môn học không hợp lệ.']
            elif field == 'rooms':
                errors[field] = ['Trường này là bắt buộc và ít nhất một phòng phải tồn tại.']
            else:
                errors[field] = messages

        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    def list(self, request, *args, **kwargs):
        queryset = self.queryset

        # Lấy các tham số tìm kiếm từ query params
        semester = request.query_params.get('semester', None)
        subject = request.query_params.get('subject', None)
        room = request.query_params.get('room', None)
        name_lesson = request.query_params.get('name_lesson', None)

        if semester:
            queryset = queryset.filter(semester=semester)
        if subject:
            queryset = queryset.filter(subject=subject)
        if room:
            queryset = queryset.filter(room=room)  # Lọc theo trường room
        if name_lesson:
            queryset = queryset.filter(name_lesson__icontains=name_lesson)

        # Kiểm tra nếu không tìm thấy kết quả nào
        if not queryset.exists():
            return Response({'message': 'Không tìm thấy bài học nào.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# lesson
class LessonViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = Lesson.objects.all() 
    serializer_class = LessonSerializer 

    @action(detail=False, methods=['post'], url_path='create_schedule')
    @transaction.atomic
    def create_schedule(self, request):
        semester = request.data.get('semester')
        room = request.data.get('room')
        weekday = request.data.get('weekday')
        period = request.data.get('period')
        subject = request.data.get('subject')

        try:
            semester = Semester.objects.get(name=semester)
        except Semester.DoesNotExist:
            return Response({"error": "Không tìm thấy kỳ học."}, status=status.HTTP_404_NOT_FOUND)

        try:
            period = Period.objects.get(number=period)
        except Period.DoesNotExist:
            return Response({"error": "Không tìm thấy tiết học."}, status=status.HTTP_404_NOT_FOUND)

        start_date = semester.day_begin
        end_date = semester.get_day_end()
        lessons_created = []
        current_date = start_date

        while current_date <= end_date:
            if current_date.weekday() == weekday:
                # Kiểm tra nếu bài học đã tồn tại
                if not Lesson.objects.filter(
                    semester=semester,
                    room_id=room,
                    subject=subject,
                    day=current_date,
                    period=period
                ).exists():
                    lesson = Lesson(
                        semester=semester,
                        subject=subject,
                        room_id=room,
                        day=current_date,
                        period=period
                    )
                    lesson.save()
                    lessons_created.append(lesson)

            current_date += timedelta(days=1)

        if lessons_created:
            serializer = LessonSerializer(lessons_created, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Không có bài học mới được tạo. Tất cả các bài học đã tồn tại."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], url_path='update')
    def update_lesson(self, request, pk=None):
        try:
            # Tìm bài học dựa trên ID
            lesson = Lesson.objects.get(pk=pk)
        except Lesson.DoesNotExist:
            return Response({"error": "Không tìm thấy bài học."}, status=status.HTTP_404_NOT_FOUND)
        data = request.data
        teacher_id = data.get('teacher')
        if teacher_id:
            try:
                teacher = Teacher.objects.get(pk=teacher_id)
                data['teacher'] = teacher.pk  
            except Teacher.DoesNotExist:
                return Response({"message": "Không tìm thấy giáo viên với ID đã cung cấp."}, status=status.HTTP_200_OK)
      
        serializer = LessonSerializer(lesson, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Cập nhật bài học thành công.", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"message": "Cập nhật không thành công.", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
     
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
    

class TeacherAssignmentViewSet(viewsets.ModelViewSet):
    queryset = TeacherAssignment.objects.all()
    serializer_class = TeacherAssignmentSerializer
    authentication_classes = []
    permission_classes = []

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        room_name = request.data.get('room')
        subject = request.data.get('subject')

        if not user_id or not room_name or not subject:
            return Response({'error': 'Missing user_id, room, or subject'}, status=status.HTTP_400_BAD_REQUEST)

        if subject not in SubjectChoices.values:
            return Response({'error': 'Invalid subject'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            teacher = Teacher.objects.get(user_id=user_id)
            room = Room.objects.get(name=room_name)

            assignment, created = TeacherAssignment.objects.update_or_create(
                room=room,
                subject=subject,
                defaults={'teacher': teacher},
            )

            if created:
                return Response({'message': 'Teacher assigned successfully.'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'Teacher assignment updated successfully.'}, status=status.HTTP_200_OK)

        except Teacher.DoesNotExist:
            return Response({'error': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)

        except Room.DoesNotExist:
            return Response({'error': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request, *args, **kwargs):
        teachers = Teacher.objects.all()
        result = []
        for teacher in teachers:
            assignments = ClassSubjectTeacherAssignment.objects.filter(teacher=teacher)
            if assignments.exists():
                rooms = [assignment.room.name for assignment in assignments]
                subject = assignments.first().subject  
            else:
                rooms = []
                subject = None

            result.append({
                'user_id': teacher.user_id,
                'rooms': rooms,
                'subject': subject
            })

        return Response(result, status=status.HTTP_200_OK)
    
# Tiết học
class PeriodViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer

    def list(self, request, *args, **kwargs):
        periods = self.get_queryset()
        serializer = self.get_serializer(periods, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        period = self.get_object()
        serializer = self.get_serializer(period)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def update(self, request, *args, **kwargs):
        period = self.get_object()
        serializer = self.get_serializer(period, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, *args, **kwargs):
        period = self.get_object()
        period.delete()
        return Response(status=204)