
# -----------------------------------------------sử dụng viewset-----------------------------------------------

from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.decorators import action
from django.db import transaction
from datetime import timedelta
from .filters import *

from accounts.models import Student,Teacher
from django.db.models import Avg

from django_filters.rest_framework import DjangoFilterBackend


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
    filter_backends = [DjangoFilterBackend]
    filterset_class = GradesFilter
    # tạo điểm
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

                    # Tạo một dictionary để gom nhóm các điểm
                    grouped_grades = {}
                    for grade in grades_query:
                        key = (grade.subject, grade.score_type, grade.semester.name)
                        if key not in grouped_grades:
                            grouped_grades[key] = {
                                "subject": grade.subject,
                                "score_type": grade.score_type,
                                "grade": [],
                                "student": grade.student.user.user_id,
                                "semester": grade.semester.name,
                            }
                        grouped_grades[key]["grade"].append(grade.grade)

                    # Chuyển đổi dictionary thành list
                    grouped_grades_list = list(grouped_grades.values())
                    return Response(grouped_grades_list, status=status.HTTP_200_OK)

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
        score_type = request.query_params.get('score_type')

        if not semester_name or not room_name or not subject or not score_type:
            return Response({'error': 'Thiếu tham số: semester_name, room_name, subject hoặc score_type.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            room = Room.objects.get(name=room_name)
            semester = Semester.objects.get(name=semester_name)

            students = room.students.all()

            # Khởi tạo các biến đếm cho từng khoảng
            count_0_05, count_05_1, count_1_15, count_15_2 = 0, 0, 0, 0
            count_2_25, count_25_3, count_3_35, count_35_4 = 0, 0, 0, 0
            count_4_45, count_45_5, count_5_55, count_55_6 = 0, 0, 0, 0
            count_6_65, count_65_7, count_7_75, count_75_8 = 0, 0, 0, 0
            count_8_85, count_85_9, count_9_95, count_95_10 = 0, 0, 0, 0

            # Lọc điểm theo học sinh, môn học, học kỳ và loại điểm
            grades = Grades.objects.filter(
                student__in=students,
                subject=subject,
                semester=semester,
                score_type=score_type
            ).values_list('grade', flat=True)

            # Duyệt qua từng điểm và phân loại vào các khoảng
            for grade in grades:
                if 0 <= grade < 0.5:
                    count_0_05 += 1
                elif 0.5 <= grade < 1.0:
                    count_05_1 += 1
                elif 1.0 <= grade < 1.5:
                    count_1_15 += 1
                elif 1.5 <= grade < 2.0:
                    count_15_2 += 1
                elif 2.0 <= grade < 2.5:
                    count_2_25 += 1
                elif 2.5 <= grade < 3.0:
                    count_25_3 += 1
                elif 3.0 <= grade < 3.5:
                    count_3_35 += 1
                elif 3.5 <= grade < 4.0:
                    count_35_4 += 1
                elif 4.0 <= grade < 4.5:
                    count_4_45 += 1
                elif 4.5 <= grade < 5.0:
                    count_45_5 += 1
                elif 5.0 <= grade < 5.5:
                    count_5_55 += 1
                elif 5.5 <= grade < 6.0:
                    count_55_6 += 1
                elif 6.0 <= grade < 6.5:
                    count_6_65 += 1
                elif 6.5 <= grade < 7.0:
                    count_65_7 += 1
                elif 7.0 <= grade < 7.5:
                    count_7_75 += 1
                elif 7.5 <= grade < 8.0:
                    count_75_8 += 1
                elif 8.0 <= grade < 8.5:
                    count_8_85 += 1
                elif 8.5 <= grade < 9.0:
                    count_85_9 += 1
                elif 9.0 <= grade < 9.5:
                    count_9_95 += 1
                elif 9.5 <= grade <= 10:
                    count_95_10 += 1

            return Response({
                "0.0-0.5": count_0_05,
                "0.5-1.0": count_05_1,
                "1.0-1.5": count_1_15,
                "1.5-2.0": count_15_2,
                "2.0-2.5": count_2_25,
                "2.5-3.0": count_25_3,
                "3.0-3.5": count_3_35,
                "3.5-4.0": count_35_4,
                "4.0-4.5": count_4_45,
                "4.5-5.0": count_45_5,
                "5.0-5.5": count_5_55,
                "5.5-6.0": count_55_6,
                "6.0-6.5": count_6_65,
                "6.5-7.0": count_65_7,
                "7.0-7.5": count_7_75,
                "7.5-8.0": count_75_8,
                "8.0-8.5": count_8_85,
                "8.5-9.0": count_85_9,
                "9.0-9.5": count_9_95,
                "9.5-10.0": count_95_10
            }, status=status.HTTP_200_OK)

        except Room.DoesNotExist:
            return Response({'error': 'Room không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)
        except Semester.DoesNotExist:
            return Response({'error': 'Học kỳ không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)
        
#-----------------------------------------------------------------------------------------------


class PlannedLessonViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = PlannedLesson.objects.all()
    serializer_class = PlannedLessonSerializer
    def get_queryset(self):
        queryset = super().get_queryset()
        
        semester = self.request.query_params.get('semester')
        room = self.request.query_params.get('room')
        subject = self.request.query_params.get('subject')
        teacher_user_id = self.request.query_params.get('user_id')

        if semester:
            queryset = queryset.filter(semester__name=semester)
        if room:
            queryset = queryset.filter(room__name=room)
        if subject:
            queryset = queryset.filter(subject=subject)
        if teacher_user_id:
            queryset = queryset.filter(teacher__user_id=teacher_user_id)

        return queryset
    
#lesson
class LessonViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = Lesson.objects.all() 
    serializer_class = LessonSerializer 
    filter_backends = [DjangoFilterBackend]
    filterset_class = LessonFilter 

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
    
# Phân công giáo viên
class TeacherAssignmentViewSet(viewsets.ModelViewSet):
    queryset = TeacherAssignment.objects.all()
    serializer_class = TeacherAssignmentSerializer
    authentication_classes = []  
    permission_classes = []  
    def create(self, request, *args, **kwargs):
        room_name = request.data.get('room')
        teacher_id = request.data.get('teacher')
        semester = request.data.get('semester')
        if not Semester.objects.filter(name=semester).exists():
            return Response({'error': 'Học kỳ không tồn tại.'}, status=status.HTTP_400_BAD_REQUEST)
        if not Room.objects.filter(name=room_name).exists():
            return Response({'error': 'Phòng học không tồn tại.'}, status=status.HTTP_400_BAD_REQUEST)
        if not Teacher.objects.filter(user_id=teacher_id).exists():
            return Response({'error': 'Giáo viên không tồn tại.'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)
    
    # có thể đặt filter.py ở đây thay vì hàm lọc 
    def get_queryset(self):
        queryset = super().get_queryset()
        teacher_user_id = self.request.query_params.get('user_id')
        room = self.request.query_params.get('room')
        subject = self.request.query_params.get('subject')
        semester = self.request.query_params.get('semester')
        if teacher_user_id:
            queryset = queryset.filter(teacher__user__user_id=teacher_user_id)
        if room:
            queryset = queryset.filter(room__name=room)
        if subject:
            queryset = queryset.filter(subject=subject)
        if semester:
            queryset = queryset.filter(semester__name=semester)
        return queryset