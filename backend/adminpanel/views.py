
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
from rest_framework.views import APIView


class SemesterViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer

    def create(self, request, *args, **kwargs):
        day_begin = request.data.get('day_begin')

        # Kiểm tra nếu ngày bắt đầu không phải là thứ Hai
        if day_begin:
            day_begin_date = date.fromisoformat(day_begin)
            if day_begin_date.weekday() != 0:  # 0 tương ứng với thứ Hai
                return Response({"error": "Ngày bắt đầu phải là thứ Hai."},
                                status=status.HTTP_400_BAD_REQUEST)

        # Nếu hợp lệ, tiến hành tạo mới học kỳ
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        # Ghi đè để thực hiện các hành động bổ sung trước khi lưu
        serializer.save()


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
            # Nếu dữ liệu là danh sách (nhiều điểm)
            if isinstance(data, list):
                for item in data:
                    student = item.get('student')
                    subject = item.get('subject')
                    semester = item.get('semester')
                    score_type = item.get('score_type')

                    # Kiểm tra nếu là điểm giữa kỳ (GK) hoặc điểm cuối kỳ (CK) và đã tồn tại
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
                # Xử lý cho trường hợp thêm một điểm duy nhất
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

            serializer.save()  # Lưu điểm
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

            # API 1: Lấy điểm của một học sinh theo từng môn
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

            # API 2: Lấy danh sách điểm học sinh theo phòng học
            elif room_name:
                try:
                    room = Room.objects.get(name=room_name)
                    students = room.students.all()

                    results = {}
                    no_scores = []  # Danh sách lưu học sinh không có điểm

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

            # API 3: Lấy danh sách top 30 học sinh theo môn học
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

# lesson
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


       
# Phân công giáo vien
# class TeacherAssignmentView(APIView):
#     authentication_classes = []
#     permission_classes = []
#     def post(self, request):
#         user_id = request.data.get('user_id')
#         room_name = request.data.get('room')
#         subject = request.data.get('subject')

#         # Kiểm tra dữ liệu đầu vào
#         if not user_id or not room_name or not subject:
#             return Response({'error': 'Missing user_id, room, or subject'}, status=status.HTTP_400_BAD_REQUEST)
        
#         # Kiểm tra subject có hợp lệ không
#         if subject not in SubjectChoices.values:
#             return Response({'error': 'Invalid subject'}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             # Lấy teacher từ user_id
#             teacher = Teacher.objects.get(user_id=user_id)

#             # Lấy room từ room_name
#             room = Room.objects.get(name=room_name)

#             # Tạo hoặc cập nhật thông tin phân công giáo viên
#             assignment, created = ClassSubjectTeacherAssignment.objects.update_or_create(
#                 room=room,
#                 subject=subject,
#                 defaults={'teacher': teacher},
#             )

#             if created:
#                 return Response({'message': 'Teacher assigned successfully.'}, status=status.HTTP_201_CREATED)
#             else:
#                 return Response({'message': 'Teacher assignment updated successfully.'}, status=status.HTTP_200_OK)

#         except Teacher.DoesNotExist:
#             return Response({'error': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)
        
#         except Room.DoesNotExist:
#             return Response({'error': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)
        
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TeacherAssignmentViewSet(viewsets.ModelViewSet):
    queryset = ClassSubjectTeacherAssignment.objects.all()
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

            assignment, created = ClassSubjectTeacherAssignment.objects.update_or_create(
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
        # Lấy tất cả giáo viên
        teachers = Teacher.objects.all()
        result = []

        # Lặp qua từng giáo viên để kiểm tra phân công
        for teacher in teachers:
            assignments = ClassSubjectTeacherAssignment.objects.filter(teacher=teacher)

            # Nếu giáo viên đã được phân công, liệt kê các lớp và môn học
            if assignments.exists():
                rooms = [assignment.room.name for assignment in assignments]
                subject = assignments.first().subject  # Giả sử 1 giáo viên chỉ dạy 1 môn
            else:
                rooms = []
                subject = None

            result.append({
                'user_id': teacher.user_id,
                'rooms': rooms,
                'subject': subject
            })

        return Response(result, status=status.HTTP_200_OK)