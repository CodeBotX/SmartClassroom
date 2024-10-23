from rest_framework import viewsets, permissions,status
from .models import Document
from .serializers import *
from rest_framework.exceptions import PermissionDenied
from .permissions import IsTeacherOrAdmin
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action



# api danh mục
class CategoryViewSet(viewsets.ModelViewSet):
    #IsTeacherOrAdmin
    authentication_classes = []
    permission_classes = []
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

