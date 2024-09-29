# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Semester, StudyWeek
# from .serializers import SemesterSerializer

# class SemesterCreateAPIView(APIView):
#     authencaiton_classes = []
#     permission_classes = []
#     def post(self, request, *args, **kwargs):
#         serializer = SemesterSerializer(data=request.data)
#         if serializer.is_valid():
#             semester_data = serializer.validated_data
#             semester = semester_data['semester']
#             day_begin = semester_data['day_begin']
#             number_of_weeks = semester_data['number_of_weeks']
#             if Semester.objects.filter(semester=semester).exists():
#                 return Response({'error': 'Semester already exists.'}, status=status.HTTP_400_BAD_REQUEST)
#             semester_instance = Semester.objects.create(
#                 semester=semester,
#                 day_begin=day_begin,
#                 number_of_weeks=number_of_weeks
#             )
#             for week_number in range(1, number_of_weeks + 1):
#                 StudyWeek.objects.create(semester=semester_instance, week_number=week_number)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# -----------------------------------------------sử dụng viewset-----------------------------------------------

from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Semester, StudyWeek
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