from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from course_materials.models import Course, Lesson, Subscription
from course_materials.paginators import MyPaginator
from course_materials.serializers import (
    CourseSerializer,
    LessonSerializer,
    CourseDetailSerializer,
)
from users.permissions import IsModer, IsOwner
from course_materials.tasks import send_info


class CourseViewSet(viewsets.ModelViewSet):
    # serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = MyPaginator

    """define which serialize to use depending on action"""

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        """this method works when user creates new course via API"""

        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        """this method checks if user belongs to moderator, user, owner and gives corresponding perms"""

        if self.action == "create":
            self.permission_classes = (~IsModer,)  # "~" not moderator
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModer | IsOwner,)

        return super().get_permissions()

    def perform_update(self, serializer):
        course = serializer.save()

        emails = []
        subscriptions = Subscription.objects.filter(course=course)
        for s in subscriptions:
            emails.append(s.user.email)

        send_info.delay(course.id, emails, f"Course {course.title} is changed")


class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        """Method works when user creates lesson via API"""

        course = serializer.save()
        course.owner = self.request.user
        course.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner | ~IsModer)


class SubscriptionView(APIView):
    """Class to check the subscription"""

    def post(self, request, course_id, *args, **kwargs):
        user = request.user  # Getting the current user

        course_item = get_object_or_404(Course, id=course_id)  # Get course or 404

        # Checking the subscription
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "subscription deleted"
        else:
            Subscription.objects.create(
                user=user, course=course_item
            )  # Creating subscription
            message = "Subscription created"

        return Response({"message": message})
