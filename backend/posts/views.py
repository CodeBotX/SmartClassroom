from rest_framework import viewsets
from .models import Post, Comment, PostFile
from .serializers import PostSerializer, CommentSerializer, PostFileSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        files_data = request.FILES.getlist('files')
        post_data = request.data.copy()
        post_data.pop('files', None)  # Remove files from data for post creation
        post = Post.objects.create(**post_data)
        
        for file in files_data:
            PostFile.objects.create(post=post, file=file)

        serializer = self.get_serializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return Response({'likes_count': post.likes.count()})