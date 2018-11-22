from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from pycoins.api.serializers.alert import AlertSerializer


class AlertList(generics.ListCreateAPIView):
    serializer_class = AlertSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.alerts.all().select_related('coin', 'currency').prefetch_related('user')

    def get_serializer_context(self):
        context = super(AlertList, self).get_serializer_context()
        context['user'] = self.request.user
        return context


class AlertDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AlertSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.alerts.all()

    def get_serializer_context(self):
        context = super(AlertDetail, self).get_serializer_context()
        context['user'] = self.request.user
        return context
