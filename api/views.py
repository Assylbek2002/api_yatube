from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import BasePermission, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Post, Comment, Follow, User, Group
from .serializers import PostSerializer, CommentSerializer, FollowSerializer, GroupSerializer
from rest_framework import filters


class IsOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ("PUT", "PATCH", "DELETE"):
            return request.user == obj.author
        return True


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerPermission]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        if 'group' in self.request.query_params.keys():
            group_id = int(self.request.query_params.get('group'))
            group = get_object_or_404(Group, id=group_id)
            posts = Post.objects.filter(group=group)
            return posts
        posts = Post.objects.all()
        return posts


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerPermission]

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=int(self.kwargs.get('post_id')))
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs.get("post_id"))
        comments = Comment.objects.filter(post=post)
        return comments


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class FollowViewSet(ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        if not ("following" in self.request.data.dict().keys()):
            raise ValidationError("Incorrect data")
        username = self.request.data.dict()["following"]
        following = get_object_or_404(User, username=username)
        if self.request.user == following:
            raise ValidationError('You can not follow yourself')
        elif Follow.objects.filter(user=self.request.user, following=following):
            raise ValidationError("You have already followed that account")
        serializer.save(user=self.request.user, following=following)
