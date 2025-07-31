from django.contrib import admin
from course_materials.models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "course_name", "description", "preview")
    list_filter = ("course_name",)
    search_fields = (
        "course_name",
        "description",
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "lesson_name",
        "description",
        "preview",
    )
    list_filter = ("lesson_name",)
    search_fields = (
        "lesson_name",
        "description",
    )
