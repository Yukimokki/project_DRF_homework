from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework.permissions import AllowAny

from users.filters import PaymentFilter
from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """allows to make CRUD views automatically"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentListView(ListCreateAPIView):
    """allows to make view list for payments and new products creation"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)


    def perform_create(self, serializer):
        """ create new user and hash their password"""
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()
