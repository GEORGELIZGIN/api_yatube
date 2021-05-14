from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Comment, Post
from .permissions import PostAndCommentPermissions
from .serializers import CommentSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [PostAndCommentPermissions]

    def create(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        post = get_object_or_404(Post, id=pk)
        self.check_object_permissions(self.request, obj=post)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            return Response(serializer.data)

    def partial_update(self, request, pk=None):
        post = get_object_or_404(Post, id=pk)
        self.check_object_permissions(self.request, obj=post)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            return Response(serializer.data)

    def destroy(self, request, pk=None):
        post = get_object_or_404(Post, id=pk)
        self.check_object_permissions(self.request, obj=post)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer
    permission_classes = [PostAndCommentPermissions]

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        return post.comments.all()

    def create(self, request, **kwargs):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            post = get_object_or_404(Post, id=kwargs.get('post_id'))
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None, **kwargs):
        comment = get_object_or_404(Comment, id=pk)
        post = get_object_or_404(Post, id=kwargs.get('post_id'))
        if not post.comments.filter(post=post).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(self.request, obj=comment)
        serializer = PostSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user, post=post)
            return Response(serializer.data)

    def partial_update(self, request, pk=None, **kwargs):
        comment = get_object_or_404(Comment, id=pk)
        post = get_object_or_404(Post, id=kwargs.get('post_id'))
        if not post.comments.filter(post=post).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(self.request, obj=comment)
        serializer = PostSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user, post=post)
            return Response(serializer.data)

    def destroy(self, request, pk=None, **kwargs):
        comment = get_object_or_404(Comment, id=pk)
        post = get_object_or_404(Post, id=kwargs.get('post_id'))
        if not post.comments.filter(post=post).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(self.request, obj=comment)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
