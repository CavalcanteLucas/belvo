from rest_framework import generics

from belvo.users.models import User
from belvo.users.serializers import UserSerializer, BalanceSerializer
from belvo.transactions.models import Transaction


class UserListAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserBalanceAPIView(generics.ListAPIView):
    serializer_class = BalanceSerializer

    def get_queryset(self):
        user_id = self.kwargs["pk"]
        return Transaction.objects.filter(user_id=user_id)
