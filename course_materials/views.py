from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from course_materials.models import Course, Lesson
from course_materials.serializers import CourseSerializer, LessonSerializer, CourseDetailSerializer
from users.permissions import IsModer, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    def get_serializer_class(self):
       if self.action == "retrieve":
           return CourseDetailSerializer
       return CourseSerializer

    def perform_create(self, serializer):
        """ this method works when user creates new course via API"""

        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        """ this method checks if user belongs to moderator, user, owner and gives corresponding perms"""

        if self.action == "create":
            self.permission_classes = (~IsModer,)  # "~" not moderator
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModer | IsOwner,)

        return super().get_permissions()

class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        """ Method works when user creates lesson via API"""

        course = serializer.save()
        course.owner = self.request.user
        course.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner | ~IsModer)