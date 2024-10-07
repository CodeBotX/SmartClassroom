
# -----------------------------------------------sử dụng viewset-----------------------------------------------

from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.db import transaction

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
        serializer = CreateLessonSerializer(data=request.data)
        if serializer.is_valid():
            semester = serializer.validated_data['semester']
            subject = serializer.validated_data['subject']
            lesson_number = serializer.validated_data['lesson_number']
            name_lesson = serializer.validated_data['name_lesson']
            rooms = serializer.validated_data['rooms']

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

    def create(self, request):
        semester_code = request.data.get("semester")
        subject = request.data.get("subject")
        weekday = request.data.get("weekday")  # 0-6 (Monday-Sunday)
        period_number = request.data.get("period")
        room_name = request.data.get("room")

        # Lấy Room object
        try:
            room = Room.objects.get(name=room_name)
        except Room.DoesNotExist:
            return Response({'error': 'Room does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        # Lấy Period object
        try:
            period = Period.objects.get(number=period_number)
        except Period.DoesNotExist:
            return Response({'error': 'Period does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        # Lấy Semester object
        try:
            semester_obj = Semester.objects.get(semester=semester_code)
        except Semester.DoesNotExist:
            return Response({'error': 'Semester does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        # Tính toán ngày học trong học kỳ
        start_date = semester_obj.day_begin
        number_of_weeks = semester_obj.number_of_weeks
        days_in_semester = [start_date + timedelta(days=i) for i in range(number_of_weeks * 7)]
        weekdays_in_semester = [day for day in days_in_semester if day.weekday() == weekday]

        with transaction.atomic():
            for day in weekdays_in_semester:
                # Kiểm tra sự tồn tại trước khi tạo
                if not Lesson.objects.filter(
                    semester=semester_obj,
                    room=room,
                    subject=subject,
                    day=day,
                    period=period
                ).exists():
                    lesson_number = self.get_next_lesson_number(semester_obj, room, subject, day, period)
                    name_lesson = self.get_lesson_name(semester_obj, subject, lesson_number)

                    Lesson.objects.create(
                        semester=semester_obj,
                        subject=subject,
                        lesson_number=lesson_number,
                        name_lesson=name_lesson,
                        room=room,
                        day=day,
                        period=period
                    )
                else:
                    print(f"Lesson already exists for {day} in room {room.name}")

        return Response({'message': 'Lessons created successfully.'}, status=status.HTTP_201_CREATED)

    def get_next_lesson_number(self, semester, room, subject):
        last_lesson = Lesson.objects.filter(
            semester=semester,
            room=room,
            subject=subject,
        ).order_by('lesson_number').last()
        return (last_lesson.lesson_number + 1) if last_lesson else 1

    def get_lesson_name(self, semester, subject, lesson_number):
        planned_lesson = PlannedLesson.objects.filter(
            semester=semester,
            subject=subject,
            lesson_number=lesson_number
        ).first()
        return planned_lesson.name_lesson if planned_lesson else "Unknown Lesson"