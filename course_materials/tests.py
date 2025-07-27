from rest_framework.test import APITestCase
from course_materials.models import Course, Lesson
from users.models import User
from django.shortcuts import reverse
from rest_framework import status


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@skypro.ru")
        self.course = Course.objects.create(
            title="New course", description="Description"
        )
        self.lesson = Lesson.objects.create(
            title="New Lesson",
            description="Description",
            video_url="link.youtube.com",
            course=self.course,
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        """Testing lesson information get"""
        url = reverse("courses:lessons_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_create(self):
        """Testing new lesson creation"""
        url = reverse("courses:lessons_create")

        # Correct information for the lesson creation
        data = {
            "title": "Урок 1",
            "course": self.course.pk,
            "description": "Описание",
            "video_url": "https://www.youtube.com/",
        }
        response = self.client.post(url, data)
        # print(response.data)
        # Checking new lesson creation
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

        # Wrong data for lesson creation
        data = {
            "title": "Lesson 1",
            "course": self.course.pk,
            "description": "Description",
            "video_url": "https://rutube.ru/",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_lesson_update(self):
        """Testing lesson update"""
        url = reverse("courses:lessons_update", args=(self.lesson.pk,))
        data = {"title": "Lesson 2"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Урок 2")

    def test_lesson_delete(self):
        """Testing Lesson deletion"""
        url = reverse("courses:lessons_destroy", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        """Testing Lesson list retrieval"""
        url = reverse("courses:lessons_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "video_url": self.lesson.video_url,
                    "title": self.lesson.title,
                    "description": self.lesson.description,
                    "preview": None,
                    "course": self.lesson.course.pk,
                    "owner": self.lesson.owner.pk,
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="admin@skyscannerru")
        self.course = Course.objects.create(
            title="awgawfawefweaf", description="sefgaesfawe"
        )
        self.client.force_authenticate(user=self.user)

    def test_subscription_post(self):
        """Testing subscription"""
        url = reverse("courses:subscribe_view", args=(self.course.pk,))
        data = {"user": self.user.pk, "course_id": self.course.pk}

        self.assertTrue(Course.objects.filter(pk=self.course.pk).exists())
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("message"), "Subscription added")

    def test_unsubscription_post(self):
        """Testing subscription letter"""

        # Adding subscription first
        url = reverse("courses:subscribe_view", args=(self.course.pk,))
        data = {"user": self.user.pk, "course_id": self.course.pk}
        self.client.post(url, data)  # Adding subscription

        # Testing subscription
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("message"), "Subscription delted")

    def test_subscription_non_existent_course(self):
        """Testing subscription for non-existing course"""
        url = reverse("courses:subscribe_view", args=(123123,))
        data = {"user": self.user.pk, "course_id": 123123}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data.get("detail"),
            "No Course matches the given query.",
        )
