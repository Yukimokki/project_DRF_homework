from django.urls import path

from course_materials.apps import CourseMaterialsConfig
from rest_framework.routers import DefaultRouter
from course_materials.views import CourseViewSet, LessonCreateAPIView, LessonRetrieveAPIView, LessonUpdateAPIView, \
    LessonDestroyAPIView, LessonListAPIView, SubscriptionView

app_name = CourseMaterialsConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses',)

urlpatterns = [
    path('lesson/create', LessonCreateAPIView.as_view(), name="Lesson_Create"),
    path('lesson', LessonListAPIView.as_view(), name="Lesson_List"),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name="Lesson_Get"),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name="Lesson_Update"),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name="Lesson_Delete"),
    path('<int:course_id>/subscribe/', SubscriptionView.as_view(), name="subscribe_view"),
] + router.urls