from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from course_materials.models import Course
from users.filters import PaymentFilter
from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer
from users.services import create_session

import stripe


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        """Creates new user and hash the password"""

        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

class PaymentViewSet(viewsets.ModelViewSet):
    """allows to make CRUD views automatically"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
#
#
# class PaymentListView(ListCreateAPIView):
#     """allows to make view list for payments and new products creation"""
#
#     queryset = Payment.objects.all()
#     serializer_class = PaymentSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_class = PaymentFilter


class PaymentListView(ListCreateAPIView):
    """Creates methods only to receive a list of objects and new objects creation"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter

    def perform_create(self, serializer):
        # Gets course_id from url request
        course_id = self.kwargs.get('course_id')
        # Get course object from ID
        course = Course.objects.get(id=course_id)
        # Saves payment with user and paid course name
        payment = serializer.save(user=self.request.user, paid_course=course)

        try:
            course_name = course.title
            session_id, payment_link = create_session(payment.payment_amount, f"to be paid {course_name}")
            payment.session_id = session_id
            payment.payment_link = payment_link
            payment.save()
        except stripe.error.StripeError as e:
            print(f"Stripe session creation error: {e}")
            raise
