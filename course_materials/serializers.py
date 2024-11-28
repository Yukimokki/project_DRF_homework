from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField
from course_materials.models import Course, Lesson

class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"

class CourseSerializer(serializers.ModelSerializer):
    lessons_count = SerializerMethodField()

    def get_lessons_count(self, course):
        return course.lessons.count()

    class Meta:
        model = Course
        fields = ("id", "course_name", "lessons_count")


class CourseDetailSerializer(ModelSerializer):

    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lessons_count(self, course):
        return course.lessons.count()

    class Meta:
        model = Course
        fields = ("course_name", "lessons_count", "lessons")