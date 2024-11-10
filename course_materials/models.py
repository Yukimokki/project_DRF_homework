from django.db import models


NULLABLE = {"blank": True, "null": True}

class Course(models.Model):
    course_name = models.CharField(max_length=100, verbose_name = "course_name", help_text = "name of the course")
    description = models.TextField(verbose_name='description')
    preview = models.ImageField(
        upload_to="course/preview",
        **NULLABLE,
        verbose_name="course preview",
        help_text="Upload course preview",
    )


    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return f'{self.course_name}{self.description}'

class Lesson(models.Model):
    lesson_name = models.CharField(max_length=100, verbose_name = "lesson_name", help_text = "name of the lesson")
    description = models.TextField(verbose_name='description')
    preview = models.ImageField(
        upload_to="lesson/preview",
        **NULLABLE,
        verbose_name="lesson preview",
        help_text="Upload lesson preview",
    )
    video_link = models.FileField(upload_to="lesson/video", **NULLABLE, max_length=254, verbose_name = "lesson video")

    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Course",
        help_text="Lesson belongs to",
        related_name="courses",
    )

    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"

    def __str__(self):
        return f'{self.lesson_name}{self.description}'
