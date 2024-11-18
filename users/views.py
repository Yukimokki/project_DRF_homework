from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView

from users.filters import PaymentFilter
from users.models import Payment
from users.serializers import PaymentSerializer


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
