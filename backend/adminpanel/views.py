
# -----------------------------------------------sử dụng viewset-----------------------------------------------

from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.decorators import action

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
        

class PlannedLessonViewSet(viewsets.ModelViewSet):
    authencation_classes = []
    permission_classes = []
    queryset = PlannedLesson.objects.all()
    serializer_class = PlannedLessonSerializer

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
    
    
class LessonCreateView(APIView):
    def post(self, request):
        serializer = LessonCreateSerializer(data=request.data)
        if serializer.is_valid():
            room = serializer.validated_data['room']
            day = serializer.validated_data['day']
            period = serializer.validated_data['period']
            subject = serializer.validated_data['subject']

            # Tìm kỳ học hiện tại
            semester = Semester.objects.get(current=True)

            # Kiểm tra xem lesson đã tồn tại hay chưa
            if Lesson.objects.filter(day=day, room=room, period=period, semester=semester).exists():
                return Response({"error": "Tiết học đã tồn tại cho thời gian và phòng này."}, status=status.HTTP_400_BAD_REQUEST)

            # Tìm danh sách PlannedLesson cho môn học đó trong kỳ học này
            planned_lessons = PlannedLesson.objects.filter(
                subject=subject,
                semester=semester
            ).order_by('lesson_number')

            if not planned_lessons.exists():
                return Response({"error": "Không tìm thấy PlannedLesson cho môn học này trong kỳ học hiện tại."}, status=status.HTTP_404_NOT_FOUND)

            # Tìm lesson_number tiếp theo dựa trên các Lesson đã có
            last_lesson = Lesson.objects.filter(
                room=room,
                planned_lesson__subject=subject,
                planned_lesson__semester=semester
            ).aggregate(Max('planned_lesson__lesson_number'))

            # Xác định lesson_number tiếp theo
            next_lesson_number = last_lesson['planned_lesson__lesson_number__max'] + 1 if last_lesson['planned_lesson__lesson_number__max'] else 1

            # Tìm PlannedLesson tương ứng với lesson_number tiếp theo
            try:
                planned_lesson = planned_lessons.get(lesson_number=next_lesson_number)
            except PlannedLesson.DoesNotExist:
                return Response({"error": "Không còn PlannedLesson nào có sẵn."}, status=status.HTTP_404_NOT_FOUND)

            # Tạo Lesson mới
            lesson = Lesson.objects.create(
                day=day,
                room=room,
                period=period,
                semester=semester,
                planned_lesson=planned_lesson
            )

            return Response({"message": "Tạo tiết học thành công.", "lesson_id": lesson.id}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)