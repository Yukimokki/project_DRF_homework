from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField
from course_materials.models import Course, Lesson, Subscription
from course_materials.validators import validate_youtube_link


class LessonSerializer(ModelSerializer):
    video_url = serializers.CharField(validators=[validate_youtube_link])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = SerializerMethodField()
    subscription = serializers.SerializerMethodField()

    def get_subscription(self, obj):
        user = self.context["request"].user
        return Subscription.objects.filter(user=user, course=obj).exists()

    def get_lessons_count(self, course):
        return course.lessons.count()

    class Meta:
        model = Course
        fields = ("id", "course_name", "lessons_count", "subscription")


class CourseDetailSerializer(ModelSerializer):

    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lessons_count(self, course):
        return course.lessons.count()

    class Meta:
        model = Course
        fields = ("course_name", "lessons_count", "lessons")
