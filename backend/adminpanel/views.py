
# -----------------------------------------------sử dụng viewset-----------------------------------------------

from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.decorators import action
from django.db import transaction
from datetime import timedelta

class SemesterViewSet(viewsets.ModelViewSet):
    authentication_classes = []  
    permission_classes = []  
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer

    def create(self, request, *args, **kwargs):
        semester = request.data.get('semester')
        if Semester.objects.filter(semester=semester).exists():
            return Response({'error': f'Học kỳ {semester} đã tồn tại.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save()
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

    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class StudyWeekViewSet(viewsets.ModelViewSet):
    authencation_classes = []
    permission_classes = []
    queryset = StudyWeek.objects.all()
    serializer_class = StudyWeekSerializer

    def create(self, request, *args, **kwargs):
        semester_id = request.data.get('semester')
        week_number = request.data.get('week_number')
        
        if StudyWeek.objects.filter(semester_id=semester_id, week_number=week_number).exists():
            return Response({'error': f'Tuần học này đã tồn tại trong học kỳ {semester_id}.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    @action(detail=False, methods=['get'])
    def find(self, request):
        semester_id = request.query_params.get('semester')
        week_number = request.query_params.get('week_number')

        if semester_id and week_number:
            try:
                study_week = StudyWeek.objects.get(semester_id=semester_id, week_number=week_number)
                serializer = self.get_serializer(study_week)
                return Response(serializer.data)
            except StudyWeek.DoesNotExist:
                return Response({'error': f'Không tìm thấy tuần {week_number} trong kỳ {semester_id}.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Bạn cần nhập vào học kỳ và tuần học."}, status=status.HTTP_400_BAD_REQUEST)
        


class LessonViewSet(viewsets.ModelViewSet):
    authencation_classes = []
    permission_classes = []
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class GradesViewSet(viewsets.ModelViewSet):
    authencation_classes = []
    permission_classes = []
    queryset = Grades.objects.all()
    serializer_class = GradesSerializer
    
    
 
    
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



# class LessonViewSet(viewsets.ModelViewSet): (chưa xong)
#     authentication_classes = []
#     permission_classes = []
#     queryset = Lesson.objects.all()
#     serializer_class = LessonSerializer

#     def create(self, request):
#         semester_code = request.data.get("semester")
#         subject = request.data.get("subject")
#         weekday = request.data.get("weekday")  
#         period_number = request.data.get("period")
#         room_name = request.data.get("room")
        
#         try:
#             room = Room.objects.get(name=room_name)
#         except Room.DoesNotExist:
#             return Response({'error': 'Room does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
#         try:
#             period = Period.objects.get(number=period_number)
#         except Period.DoesNotExist:
#             return Response({'error': 'Period does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
#         try:
#             semester_obj = Semester.objects.get(semester=semester_code)
#         except Semester.DoesNotExist:
#             return Response({'error': 'Semester does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

#         start_date = semester_obj.day_begin
#         number_of_weeks = semester_obj.number_of_weeks
#         days_in_semester = [start_date + timedelta(days=i) for i in range(number_of_weeks * 7)]
#         weekdays_in_semester = [day for day in days_in_semester if day.weekday() == weekday]

#         # Lấy tất cả lesson hiện tại cho môn học này trong học kỳ
#         existing_lessons = Lesson.objects.filter(semester=semester_obj, subject=subject, room=room)
#         existing_lesson_numbers = [lesson.lesson_number for lesson in existing_lessons]

#         with transaction.atomic():
#             for day in weekdays_in_semester:
#                 if not Lesson.objects.filter(
#                     semester=semester_obj,
#                     room=room,
#                     subject=subject,
#                     day=day,
#                     period=period
#                 ).exists():
#                     # Tính lesson_number mới
#                     lesson_number = max(existing_lesson_numbers, default=0) + 1
#                     existing_lesson_numbers.append(lesson_number)  # Cập nhật danh sách lesson_number đã tồn tại
#                     name_lesson = self.get_lesson_name(semester_obj, subject, lesson_number)

#                     Lesson.objects.create(
#                         semester=semester_obj,
#                         subject=subject,
#                         lesson_number=lesson_number,
#                         name_lesson=name_lesson,
#                         room=room,
#                         day=day,
#                         period=period
#                     )
#                 else:
#                     print(f"Lesson already exists for {day} in room {room.name}")

#         return Response({'message': 'Lessons created successfully.'}, status=status.HTTP_201_CREATED)
#     def get_lesson_name(self, semester, subject, lesson_number):
#         planned_lesson = PlannedLesson.objects.filter(
#             semester=semester,
#             subject=subject,
#             lesson_number=lesson_number
#         ).first()
#         return planned_lesson.name_lesson if planned_lesson else "Unknown Lesson"

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
            semester = Semester.objects.get(semester=semester_id)
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
