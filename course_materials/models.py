from django.db import models


NULLABLE = {"blank": True, "null": True}

class Course(models.Model):
    course_name = models.CharField(
        max_length=100,
        verbose_name = "course_name",
        help_text = "name of the course")

    description = models.TextField(verbose_name='description')

    preview = models.ImageField(
        upload_to="course/preview",
        **NULLABLE,
        verbose_name="course preview",
        help_text="Upload course preview",
    )

    owner = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name="Владелец",
        help_text="Укажите владельца курса"
    )


    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return f'{self.course_name}{self.description}'

class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Course name",
        related_name="lessons",
        **NULLABLE
    )
    lesson_name = models.CharField(
        max_length=100,
        verbose_name = "lesson_name",
        help_text = "name of the lesson")

    description = models.TextField(verbose_name='description')
    preview = models.ImageField(
        upload_to="lesson/preview",
        **NULLABLE,
        verbose_name="lesson preview",
        help_text="Upload lesson preview",
    )
    video_link = models.FileField(upload_to="lesson/video", **NULLABLE, max_length=254, verbose_name = "lesson video")


    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"

    def __str__(self):
        return f'{self.lesson_name}{self.description}'
