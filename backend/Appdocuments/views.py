from rest_framework import viewsets, permissions,status
from .models import Document
from .serializers import *
from rest_framework.exceptions import PermissionDenied
from .permissions import IsTeacherOrAdmin
from rest_framework.response import Response

class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsTeacherOrAdmin]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def perform_create(self, serializer):
        try:
            category = serializer.save()
            return Response({
                'message': 'Category created successfully.',
                'category': CategorySerializer(category).data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                'message': 'Category creation failed.',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    def perform_update(self, serializer):
        category = serializer.save()
        return Response({
            'message': 'Category updated successfully.',
            'category': CategorySerializer(category).data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({
            'message': 'Category deleted successfully.'
        }, status=status.HTTP_204_NO_CONTENT)

class DocumentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsTeacherOrAdmin]
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def perform_create(self, serializer):
        document = serializer.save(author=self.request.user)
        return Response({
            'message': 'Document created successfully.',
            'document': DocumentSerializer(document).data
        }, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        document = serializer.save()
        return Response({
            'message': 'Document updated successfully.',
            'document': DocumentSerializer(document).data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({
            'message': 'Document deleted successfully.'
        }, status=status.HTTP_204_NO_CONTENT)